#!/usr/bin/env python3

from optparse import OptionParser
import os
import sys
import json
import logging

from collections import defaultdict, deque

from confluent_kafka import Producer
from cronut import App
from cronut.utils import uriparse

from ligo.lw import lsctables

from lal import GPSTimeNow

from ligo.scald.io import kafka

from gw.lts import utils

def parse_command_line():

	parser = utils.add_general_opts()
	opts, args = parser.parse_args()

	return opts, args

def main():
	opts, args = parse_command_line()
	
	tag = opts.tag
	
	# set up producer
	client = kafka.Client(f'kafka://{tag}@{opts.kafka_server}')
	
	# set up logging
	utils.set_up_logger(opts.verbose)
	
	# initialize data deque and output dict
	output = defaultdict(lambda: {'time': [], 'data': []})
	data = deque(maxlen=300)
	
	# create a job service using cronut
	store_likelihood = App('store_likelihood', broker=f'kafka://{tag}_store_likelihood@{opts.kafka_server}')
	
	# subscribes to a topic
	@store_likelihood.process([f'{opts.data_source}.{tag}.testsuite.{topic}' for topic in opts.input_topic])
	def process(message): 
		mtopic = message.topic()
		mkey = utils.parse_msg_key(message)
		logging.debug(f'Read message from {mtopic}.')
	
		# dont process noninjection events
		if not mkey == 'noninj':
			# parse event info
			event = json.loads(message.value())
	
			coinc_file = utils.load_xml(event['coinc'])
			far = event['far']
			snr = event['snr']
			time = event['time'] + event['time_ns'] * 10**-9.
	
			# load likelihood from coinc event table
			event_table = lsctables.CoincTable.get_table(coinc_file)
			likelihood = event_table[0].likelihood
	
			# output message
			output['likelihood']['time'].append(float(time))
			output['likelihood']['data'].append(float(likelihood))
	
			# send message to output topics
			for key in output:
				client.write(f'{opts.data_source}.{tag}.testsuite.{key}', output[key])
				logging.info(f'Sent output message to output topic: {opts.data_source}.{tag}.testsuite.{key}.')

	# start up
	logging.info('Starting up...')
	store_likelihood.start()

if __name__ == '__main__':
	main()
