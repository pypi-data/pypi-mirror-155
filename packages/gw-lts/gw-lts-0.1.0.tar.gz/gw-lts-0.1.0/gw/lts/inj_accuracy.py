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

from ligo.scald.io import kafka

from gw.lts import utils

def parse_command_line():
	parser = utils.add_general_opts()

	parser.add_option('--ifo', help = 'The interferometer data to get recovered injections from. Required.')
	parser.add_option('--input-params', default = [], action = 'append', help = 'Parameters from sim inspiral table to test recovery. Can be given multiple times.')
	opts, args = parser.parse_args()

	return opts, args

def find_sngl_row(ifo, table):
	for i, row in enumerate(table):
		if table.getColumnByName('ifo')[i] == ifo:
			return i
	return None

def end_time_accuracy(simtable, sngltable, index):
	try:
		injected_time = simtable.getColumnByName('geocent_end_time')[0] + 10.**-9. * simtable.getColumnByName('geocent_end_time_ns')[0]
		recovered_time = sngltable.getColumnByName('end_time')[index] + 10.**-9. * sngltable.getColumnByName('end_time_ns')[index]

		# calculate difference in ms
		diff = (recovered_time - injected_time) * 10**3.
	except Exception as e:
		logging.debug(f'Error getting end time difference: {e}')
		diff = None

	return diff

def fractional_param_accuracy(param, ifo, simtable, sngltable):
	# find this ifo in the sngl table,
	# if this ifo is not  in the sngl table,
	# dont bother continuing
	idx = find_sngl_row(ifo, sngltable)
	if idx is None:
		return None

	# end time is handled differently because
	# we just want the difference in ms
	if param == 'end_time':
		accuracy = end_time_accuracy(simtable, sngltable, idx)
		return accuracy

	inj_param = None
	rec_param = None
	frac_accuracy = None

	# first get the injected parameter value 
	# from the sim inspiral table
	try:
		inj_param = simtable.getColumnByName(param)[0]
	except Exception as e:
		logging.debug(f'Error getting {param} from sim table: {e}')
	if inj_param is None:
		# some parameters can be computed if they are missing
		if param == 'eta':
			mass1 = simtable.getColumnByName('mass1')[0]
			mass2 = simtable.getColumnByName('mass2')[0]
			inj_param = utils.eta_from_m1_m2(mass1, mass2)
		elif param == 'mchirp':
			mass1 = simtable.getColumnByName('mass1')[0]
			mass2 = simtable.getColumnByName('mass2')[0]
			inj_param = utils.mchirp_from_m1_m2(mass1, mass2)

	# get the recovered parameter value
	# from the sngl inspiral table
	try:
		rec_param = sngltable.getColumnByName(param)[idx]
	except Exception as e:
		logging.debug(f'Error getting {param} from sngl table: {e}')

	# calculate fractional accuracy
	if rec_param and inj_param:
		frac_accuracy = 1. - (rec_param - inj_param) / inj_param
		logging.debug(f'{param}: rec: {rec_param} | inj: {inj_param} | accuracy: {frac_accuracy}')

	return frac_accuracy

def main():
	opts, args = parse_command_line()
	
	# sanity check input options
	required_opts = ['ifo', 'tag', 'input_params']
	for r in required_opts:
		if not getattr(opts, r):
			raise ValueError(f'Missing option: {r}.')
	
	ifo = opts.ifo
	tag = opts.tag
	
	# set up producer
	client = kafka.Client(f'kafka://{tag}@{opts.kafka_server}')
	
	# set up logging
	utils.set_up_logger(opts.verbose)
	
	# create a job service using cronut
	inj_accuracy = App('inj_accuracy', broker=f'kafka://{tag}_{ifo}-inj-accuracy@{opts.kafka_server}')
	
	# subscribes to a topic
	@inj_accuracy.process(opts.input_topic)
	def process(message): 
		mtopic = message.topic().split('.')[-1]
		mpipeline = message.topic().split('.')[0]
		mkey = utils.parse_msg_key(message)
		logging.info(f'Read message from input {mtopic}.')
	
		# dont process noninjection events
		if not mkey == 'noninj':
			# parse event info
			event = json.loads(message.value())
	
			coinc_file = utils.load_xml(event['coinc'])
			time = event['time'] + event['time_ns'] * 10**-9.
	
			# load sim inspiral and sngl inspiral tables
			SimInspiralTable = lsctables.SimInspiralTable.get_table(coinc_file)
			SnglInspiralTable = lsctables.SnglInspiralTable.get_table(coinc_file)
	
			for param in opts.input_params:
				# grab info from coinc file
				acc = fractional_param_accuracy(param, ifo, SimInspiralTable, SnglInspiralTable)
	
				# produce output message
				if acc is not None:
					output = {
							'time': [ float(time) ],
							'data': [ acc ]
					}
	
					client.write(f'{mpipeline}.{tag}.testsuite.{ifo}_{param}', output)
					logging.info(f'Sent msg to: {mpipeline}.{tag}.testsuite.{ifo}_{param}')
	# start up
	logging.info('Starting up...')
	inj_accuracy.start()

if __name__ == '__main__':
	main()
