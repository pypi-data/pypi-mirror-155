#!/usr/bin/env python3

from optparse import OptionParser
import os
import sys
import json
import numpy
import copy
import logging

from time import sleep
from collections import defaultdict, deque
from confluent_kafka import Producer

from cronut import App
from cronut.utils import uriparse

from ligo.lw import lsctables
from lal import GPSTimeNow
from lal import LIGOTimeGPS

from ligo.scald.io import kafka

from gw.lts import utils

def parse_command_line():
	parser = utils.add_general_opts()
	parser.add_option('--ifo', help = 'Interferometer to get data from')
	opts, args = parser.parse_args()

	return opts, args

def process_msgs(recovered, injected, pipeline):
	# for each reecovered msg time in the deque
	# find the nearest injection in injected msgs deque
	# within +/- delta_t (1 second) of the recovered msg
	# time. When an association is made, remove the recovered
	# msg from the deque, calculate the snr accuracy and
	# send a message to the output topic
	recovered_copy = copy.copy(recovered)
	for rec in recovered_copy:

		rec_time = rec['time']
		rec_snr = rec['snr']

		nearest_inj = utils.find_nearest_msg(injected, rec_time)

		if not nearest_inj:
			continue

		inj_time = nearest_inj['time']
		inj_snr = nearest_inj['snr']

		recovered.remove(rec)

		accuracy = 1. - (inj_snr - rec_snr) / inj_snr

		output = {
				'time': [ inj_time ],
				'data': [ accuracy ]
		}

		client.write(f'{pipeline}.{tag}.testsuite.{ifo}_snr_accuracy', output)
		logging.info(f'Sent msg to: {pipeline}.{tag}.testsuite.{ifo}_snr_accuracy')

def main():
	opts, args = parse_command_line()
	
	# sanity check input options
	required_opts = ['ifo', 'tag', 'input_topic', 'kafka_server']
	for r in required_opts:
		if not getattr(opts, r):
			raise ValueError(f'Missing option: {r}.')
	
	ifo = opts.ifo
	tag = opts.tag
	topics = opts.input_topic
	
	# set up producer
	client = kafka.Client(f'kafka://{tag}@{opts.kafka_server}')
	
	# set up logging
	utils.set_up_logger(opts.verbose)
	
	# initialize data deque and output dict
	data = defaultdict(lambda: defaultdict(lambda: deque(maxlen=300)))
	
	# create a job service using cronut
	snr_consistency = App('snr_consistency', broker=f'kafka://{tag}_{ifo}-snr-consistency@{opts.kafka_server}')
	
	# subscribes to a topic
	@snr_consistency.process(topics)
	def process(message):
		mifo, mtopic = message.topic().split('.')[-1].split('_')
		mpipeline = message.topic().split('.')[0]
		mkey = message.key().decode('utf-8')
	
		source, is_recovered = mkey.split('.')
		logging.info(f'Read message from input {mpipeline} {mtopic}: {source} {is_recovered}')
	
		# unpack data from the message 
		# store SNRs in a dictionary keyed by event time
		m = json.loads(message.value())
		val = m['data'][-1]
		time = m['time'][-1]
	
		if is_recovered == 'missed':
			logging.debug(f"Injection at {time} missed, skipping.")
		else:
			time_window = utils.event_window(time)
	
			data[mpipeline][mtopic].append({
							'time': time,
							'snr': val
			})
	
			process_msgs(data[mpipeline]['recsnr'], copy.deepcopy(data[mpipeline]['injsnr']), mpipeline)

	# start up
	logging.info('Starting up...')
	snr_consistency.start()

if __name__ == '__main__':
	main()
