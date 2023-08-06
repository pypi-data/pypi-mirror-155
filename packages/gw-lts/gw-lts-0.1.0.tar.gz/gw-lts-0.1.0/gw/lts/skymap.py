#!/usr/bin/env python3

from optparse import OptionParser
import os
import sys
import json
import logging
import copy

from collections import defaultdict, deque

from confluent_kafka import Producer
from cronut import App
from cronut.utils import uriparse
from io import BytesIO

from ligo.lw import lsctables
from ligo.lw.utils import load_fileobj

from lal import GPSTimeNow

from ligo.gracedb.rest import GraceDb

from ligo.skymap.bayestar import localize
from ligo.skymap.io import events as LIGOSkymapEvents
from ligo.skymap.io import read_sky_map
from ligo.skymap.postprocess import crossmatch

from astropy.coordinates import SkyCoord
from astropy.table import Table

from ligo.scald.io import kafka

from gw.lts import utils

def parse_command_line():
	parser = utils.add_general_opts()
	parser.add_option('--output', help = 'Output directory to write skymap fits files to.')
	parser.add_option('--gdb-skymaps', action='store_true', default = False, help = 'Use skymaps from GraceDB instead of calculating them manually.')
	opts, args = parser.parse_args()

	return opts, args

def process_event(event, tag=None):
	# either download skymap from gracedb or
	# generate one with bayestar
	if opts.gdb_skymaps:
		skymap = get_gracedb_skymap(event)
	else:
		skymap = make_skymap(event)

	if skymap:
		# get right ascension and declination
		# from sim inspiral table
		coinc = utils.load_xml(event['coinc'])
		simtable = lsctables.SimInspiralTable.get_table(coinc)
		ra, dec = simtable[0].ra_dec

		# use SkyCoord and crossmatch to get pvalues
		loc = SkyCoord(ra=ra, dec=dec, unit="rad")
		p = crossmatch(skymap, loc).searched_prob
		deg2 = crossmatch(skymap, loc).searched_area

		logging.debug(f'Searched probability: {p} | searched area: {deg2}')

		# construct output dict and send messages to kafka
		time = event['time']
		pipeline = event['pipeline']

		output['searched_prob'] = {
			'time': [ time ],
			'data': [ p ]
		}
		output['searched_area'] = {
			'time': [ time ],
			'data': [ deg2 ]
		}

		for key, value in output.items():
			client.write(f'{pipeline}.{tag}.testsuite.{key}', value, tags = key)
			logging.info(f'Sent msg to: {pipeline}.{tag}.testsuite.{key}')

		return True

	else:
		return False

def make_skymap(event):
	skymap = None
	coinc_obj = BytesIO(event['coinc'].encode())
	# make a copy of coinc file to avoid I/O error in events.ligolw.open()
	psd_obj = copy.copy(coinc_obj)

	event_source = LIGOSkymapEvents.ligolw.open(coinc_obj, psd_file=psd_obj, coinc_def=None)

	if len(event_source) > 1:
		logging.info('Warning: len(event_source) > 1, defaulting to use the first event.')

	# produce the skymap
	for event_id, event in event_source.items():
		skymap = localize(event)
		# break out of the loop after computing just one skymap
		# in case there are multiple rows in coinc inspiral we just
		# go with the first one
		break

	return skymap

def get_gracedb_skymap(event):
	pipeline = event['pipeline']
	time = event['time']

	query = f'{time - 1.} .. {time + 1.} pipeline: {pipeline}'
	event = next(gracedb_client.events(query))

	try:
		response = gracedb_client.files(event['graceid'], 'bayestar.multiorder.fits')
		skymap = response.read()

		filename = os.path.join(opts.output, f'{tag}-{int(time)}.fits')
		with open(filename, 'wb') as f:
			f.write(skymap)

		skymap = Table.read(filename)
	except Exception as e:
		logging.debug(f'error: {e}')
		logging.info(f'Couldnt get skymap from {pipeline} event at {time}')
		skymap = None

	return skymap

def main():
	opts, args = parse_command_line()
	
	tag = opts.tag
	datasource = opts.data_source
	# make a dir for skymaps
	if not os.path.exists(opts.output):
		os.makedirs(opts.output)
	
	if opts.gdb_skymaps:
		gracedb_client = GraceDb(service_url=f'https://{opts.group}.ligo.org/api/')
	
	# set up producer
	client = kafka.Client(f'kafka://{tag}@{opts.kafka_server}')
	
	# set up logging
	utils.set_up_logger(opts.verbose)
	
	output = defaultdict(lambda: {'time': [], 'data': []})
	events = deque(maxlen=10)
	
	# create a job service using cronut
	skymap_service = App('skymap_service', broker=f'kafka://{tag}_skymap_service@{opts.kafka_server}')
	
	# subscribes to a topic
	@skymap_service.process(opts.input_topic)
	def process(message): 
		mtopic = message.topic().split('.')[-1]
		mpipeline = message.topic().split('.')[0]
		mkey = utils.parse_msg_key(message)
		logging.info(f'Read message from {mpipeline} {mtopic}.')
	
		if not mkey == 'noninj':
			# parse event info
			event = json.loads(message.value())
			time = event['time'] + event['time_ns'] * 10**-9.
			event.update({'pipeline': mpipeline})
	
			# process the eventt - get a skymap and calculate
			# searched area and probability, send messages to
			# kafka
			response = process_event(event, tag=tag)
			if not response:
				# keep track of events that failed
				# to get a skymap on the first try
				# when getting skymaps from gracedb, this
				# can happen if the skymap isnt uploaded
				# immediately
				times = [event["time"] for event in events]
				if not event["time"] in times:
					events.append(event)
	
			# iterate over events and try again to grab a
			# skymap for each one. On success, remove the
			# event from the deque
			for event in copy.deepcopy(events):
				response = process_event(event, tag=tag)
				if response:
					events.remove(event)

	# start up
	logging.info('Starting up...')
	skymap_service.start()

if __name__ == '__main__':
	main()
