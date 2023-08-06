#!/usr/bin/env python3

import json
import logging
from gw.lts import utils
import io
import http.client

from igwn_alert.client import client as IGWNAlertClient

from ligo.lw import ligolw
from ligo.lw import lsctables
from ligo.lw import utils as ligolw_utils

from optparse import OptionParser
from confluent_kafka import Producer

from ligo.gracedb.rest import GraceDb
from ligo.gracedb.exceptions import HTTPError

from collections import OrderedDict, deque

from ligo.scald.io import kafka

from lal import GPSTimeNow

class LIGOLWContentHandler(ligolw.LIGOLWContentHandler):
	pass

lsctables.use_in(LIGOLWContentHandler)

def parse_command_line():
	parser = utils.add_general_opts()
	parser.add_option('--gdb-topics', metavar='string', action = 'append', help = 'GraceDb topics to subscribe to. Can be given multiple times.')
	parser.add_option('--max-wait-time', metavar = 'float', default = 3600., help = 'Max amount of time to keep events before removing them, whether or not a message has been sent')
	opts, args = parser.parse_args()
	return opts, args

def main():
	# parse command line
	opts, args = parse_command_line()
	
	## set up logging
	utils.set_up_logger(opts.verbose)

	# set up listener
	listener = on_alert(group=opts.group, tag=opts.tag, kafka_server=opts.kafka_server, max_wait_time = opts.max_wait_time)

	# initialize a client and listener
	client = IGWNAlertClient(group=opts.group)

	client.listen(listener.process_alert, opts.gdb_topics)

class on_alert(object):
	def __init__(self, group, tag, kafka_server, max_wait_time):
		self.group = group
		self.tag = tag
		self.gdb_client = GraceDb(service_url=f'https://{group}.ligo.org/api')
		self.max_wait_time = max_wait_time
		self.inj_channels = set(['GDS-CALIB_STRAIN_INJ1_O3Replay', 'GDS-CALIB_STRAIN_INJ1_O3Replay', 'Hrec_hoft_16384Hz_INJ1_O3Replay'])

		# set up producer
		self.client = kafka.Client(f'kafka://{tag}@{kafka_server}')

		self.events = OrderedDict()
		self.events_sent = deque(maxlen=300)

		logging.info('Initialized on_alert class.')

	def process_alert(self, topic=None, payload=None):
		# unpack data
		uid = payload['uid']	
		alert_type = payload['alert_type']
		data = payload['data']
		object = payload['object']

		channels = self.get_channels(uid)
		if not channels or not channels.issubset(self.inj_channels):
			logging.debug(f'{uid} not from injection channels, skipping.')
			return

		# find the pipeline that uploaded this event
		# this is encoded in the output topic when the message is sent
		pipeline = topic.split("_")[1]

		if alert_type == 'log' or alert_type ==  'new':
			logging.info(f'Received {alert_type} alert for {uid} from {pipeline}')

		if uid in self.events.keys():
			self.events[uid] = self.process_event(uid, output=self.events[uid])
		else:
			self.events[uid] = self.process_event(uid)

		# check if all elements present, then send msg
		# only send msg once per event
		if all(self.events[uid].values()) and not uid in self.events_sent:
			logging.info(f'sending a message for {uid} (coa time: {self.events[uid]["time"]})...')
			self.client.write(f'{pipeline}.{self.tag}.inj_events', self.events[uid])
			logging.info(f'Sent msg to: {topic}')
			self.events_sent.append(uid)

		# remove old msgs that already had a msg sent
		time_now = float(GPSTimeNow())
		for key, value in list(self.events.items()):
			if time_now - value['time_added'] >= self.max_wait_time:
				logging.debug(f'Removing old event: {key}')
				self.events.pop(key)

	def process_event(self, uid, output={}):
		if not output:
			# initialize all the items we need in order to send a message
			for k in ['time', 'time_ns', 'snr', 'far', 'coinc', 'p_astro', 'latency']:
				output.update({k: None})
			output.update({'time_added': float(GPSTimeNow())})

		output.update(self.add_coinc(uid))
		output.update(self.add_pastro(uid))
		output.update(self.add_latency(uid))

		return output

	def add_coinc(self, uid, output={}):
		coinc = self.get_filename(uid, 'coinc.xml')
		if coinc:
			xmldoc = utils.load_xml(coinc)
			coinctable = lsctables.CoincInspiralTable.get_table(xmldoc)

			coinc_msg = io.BytesIO()
			ligolw_utils.write_fileobj(xmldoc, coinc_msg, gz = False)

			output.update({
					'time': coinctable[0].end_time,
					'time_ns': coinctable[0].end_time_ns,
					'snr': coinctable[0].snr,
					'far': coinctable[0].combined_far,
					'coinc': coinc_msg.getvalue().decode()
			})	
			logging.debug(f'Added coinc.xml to {uid}')
		return output

	def add_pastro(self, uid, output = {}):
		pastro = self.get_filename(uid, 'p_astro.json')
		if pastro:
			pastro = pastro.read().decode("utf-8")
			output.update({
					'p_astro': pastro
			})
			logging.debug(f'Added p_astro.json to {uid}.')
		return output

	def add_latency(self, uid, output = {}, retries=10):
		this_try = 0
		while this_try < retries:
			try:
				event = self.gdb_client.event(uid)
				event = event.json()
				output.update({
						'latency': event['reporting_latency']
				})
				logging.debug(f'Added latency: {event["reporting_latency"]}')
				return output
			except HTTPError:
				this_try += 1
		logging.debug(f'Failed to retrieve {uid} latency from {self.group}.')
		return None

	def get_channels(self, uid):
		coinc = self.get_filename(uid, 'coinc.xml')
		if coinc:
			xmldoc = utils.load_xml(coinc)
			sngltable = lsctables.SnglInspiralTable.get_table(xmldoc)
			channels = set(list(sngltable.getColumnByName('channel')))

			return channels
		return None

	def get_filename(self, uid, filename, retries=10):
		this_try = 0
		while this_try < retries:
			try:
				response = self.gdb_client.files(uid, filename)
				if response.status == http.client.OK:
					return response
			except HTTPError:
				this_try += 1
		logging.debug(f'Failed to download {filename} from {uid}.')
		return None

if __name__ == '__main__':
	main()
