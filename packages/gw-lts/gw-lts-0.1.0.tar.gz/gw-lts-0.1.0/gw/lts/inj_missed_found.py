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

	parser.add_option('--far-threshold', default=2.314e-5, help = 'far threshold for missed vs found injections. Default is 2 per day.')
	opts, args = parser.parse_args()

	return opts, args

def construct_output(injected_snrs = {}, recovered_snrs = {}, time = None, decisive_snr = None):
	output = defaultdict(lambda: {'time': [], 'data': []})

	for ifo, value in injected_snrs.items():
		if not value:
			continue
		output[f'{ifo}_injsnr'] = {
			'time': [ time ],
			'data': [ value ]
		}

	for ifo, value in recovered_snrs.items():
		if not value:
			continue
		output[f'{ifo}_recsnr'] = {
			'time': [ time ],
			'data': [ value ]
		}

	output['decisive_snr'] = {
			'time': [ time ],
			'data': [decisive_snr]
	}

	return output

def process_event(coinc_file, on_ifos, key):
		snrs = defaultdict(lambda: 0)

		# load coinc file and get data
		coinctable = lsctables.CoincInspiralTable.get_table(coinc_file)
		sngltable = lsctables.SnglInspiralTable.get_table(coinc_file)

		coinc_time = coinctable[0].end_time + 10.**-9 * coinctable[0].end_time_ns
		for r in sngltable:
			snrs[r.ifo] = r.snr

		# get inj SNR information
		if key == 'noninj':
			inj_time = None
			inj_snrs = defaultdict(lambda: 0)
			source = key
		else:
			inj_time, inj_snrs, dec_snr, source = process_injection(coinc_file, on_ifos)

		return snrs, inj_snrs, dec_snr, source, inj_time

def process_injection(xmldoc, on_ifos):
	inj_snrs = defaultdict(lambda: None)

	simtable = lsctables.SimInspiralTable.get_table(xmldoc)

	time = simtable[0].geocent_end_time + 10.**-9 * simtable[0].geocent_end_time_ns
	inj_snrs['H1'] = simtable[0].alpha4
	inj_snrs['L1'] = simtable[0].alpha5
	inj_snrs['V1'] = simtable[0].alpha6

	source = utils.source_tag(simtable)

	dec_snr = utils.decisive_snr(inj_snrs, on_ifos)

	return time, inj_snrs, dec_snr, source

def main():
	opts, args = parse_command_line()
	
	tag = opts.tag
	topics = opts.input_topic
	datasource = opts.data_source
	far_threshold = float(opts.far_threshold)
	
	# set up producer
	client = kafka.Client(f'kafka://{tag}@{opts.kafka_server}')
	
	# set up logging
	utils.set_up_logger(opts.verbose)
	
	# create a job service using cronut
	inj_missed_found = App('inj_missed_found', broker=f'kafka://{tag}_inj-missed-found@{opts.kafka_server}')

	# subscribes to a topic
	@inj_missed_found.process(topics)
	def process(message): 
		mtopic = message.topic().split('.')[-1]
		mpipeline = message.topic().split('.')[0]
		mkey = utils.parse_msg_key(message)
	
		if mtopic == 'missed_inj':
			# these are injections that never got an event from the search
			# so they are automatically missed
			is_recovered = 'missed'
	
			injection = json.loads(message.value())
			sim_file = utils.load_xml(injection['sim'])
			on_ifos = injection['onIFOs']
	
			time, inj_snrs, dec_snr, source = process_injection(sim_file, on_ifos)
	
			logging.info(f'{mpipeline}: {source} injection from time {time} {is_recovered.upper()}: no associated event message received.')
	
			output = construct_output(injected_snrs = inj_snrs, time = time, decisive_snr = dec_snr)
			for topic in output:
				client.write(f'{mpipeline}.{tag}.testsuite.{topic}', output[topic], tags = [source, is_recovered])
				logging.info(f'Sent msg to: {topic} with tags: {source}, {is_recovered}')
	
		# otherwise, grab the coinc file, far, snr and time from the message
		# unpack data from the message, parse event info, and produce an output message
		elif mtopic == 'events':
			event = json.loads(message.value())
	
			coinc_file = utils.load_xml(event['coinc'])
			far = event['far']
			time = event['time'] + event['time_ns'] * 10**-9.
			ifos = event['onIFOs']
	
			# determine missed or found by getting the far of the recovered event
			is_recovered = 'found' if far < far_threshold else 'missed'
	
			snrs, inj_snrs, dec_snr, source, inj_time = process_event(coinc_file, ifos, mkey)
			logging.info(f'{mpipeline}: {source} event from time {time} {is_recovered.upper()}: far = {far}.')
	
			# send messages to output topics
			output = construct_output(injected_snrs = inj_snrs, recovered_snrs = snrs, time = time, decisive_snr = dec_snr)
			for topic in output:
				client.write(f'{mpipeline}.{tag}.testsuite.{topic}', output[topic], tags = [source, is_recovered])
				logging.info(f'Sent msg to: {topic} with tags: {source}, {is_recovered}')

	
	# start up
	logging.info('Starting up...')
	inj_missed_found.start()

if __name__ == '__main__':
	main()
