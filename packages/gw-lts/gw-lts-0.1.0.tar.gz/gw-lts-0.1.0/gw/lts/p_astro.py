#!/usr/bin/env python3

from optparse import OptionParser
import json
import logging

from collections import defaultdict

from confluent_kafka import Producer
from cronut import App
from cronut.utils import uriparse

from gw.lts import utils

from ligo.scald.io import kafka

from ligo.lw import lsctables

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
	
	# initialize output dict
	output = defaultdict(lambda: defaultdict(lambda: {'time': [], 'data': []}))
	
	# create a job service using cronut
	store_pastro = App('store_pastro', broker=f'kafka://{tag}_store_pastro@{opts.kafka_server}')
	
	# subscribes to a topic
	@store_pastro.process(opts.input_topic)
	def process(message): 
		mtopic = message.topic().split('.')[-1]
		mpipeline = message.topic().split('.')[0]
		mkey = utils.parse_msg_key(message)
		logging.debug(f'Read message from {mpipeline} {mtopic}.')
	
		# dont process noninjection events
		if not mkey == 'noninj':
			# get coinc_file
			event = json.loads(message.value())
			coinc_file = utils.load_xml(event['coinc'])
	
			# determine source from inspiral table
			simtable = lsctables.SimInspiralTable.get_table(coinc_file)
			source = utils.source_tag(simtable)
	
			# parse event info
			time = event['time'] + event['time_ns'] * 10**-9.
	
			p_astro_dict = json.loads(event['p_astro'])
			p_astro_dict['p_astro'] = 1-p_astro_dict['Terrestrial']
	
			# create message
			for key,value in p_astro_dict.items():
				output[source]['p_'+key]['time'].append(float(time))
				output[source]['p_'+key]['data'].append(float(value))
	
			# send message to output topics
			for topic, data in output[source].items():
				client.write(
					f'{mpipeline}.{tag}.testsuite.{topic}',
					{
						'time': [ data['time'][-1] ],
						'data': [ data['data'][-1] ]
					},
					tags = source
				)
				logging.debug(f'Inj with masses: m1 = {simtable[0].mass1}, m2 = {simtable[0].mass2} | tag: {source}')
				logging.info(f'Sent output message to output topic: {mpipeline}.{tag}.testsuite.{topic}.')

	# start up
	logging.info('Starting up...')
	store_pastro.start()

if __name__ == '__main__':
	main()
