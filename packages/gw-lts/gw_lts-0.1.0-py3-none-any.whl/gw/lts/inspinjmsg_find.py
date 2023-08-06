#!/usr/bin/env python3

from optparse import OptionParser
import os
import io
import sys
import json
import copy
import logging

from collections import defaultdict, deque, OrderedDict

from confluent_kafka import Producer
from cronut import App
from cronut.utils import uriparse

from ligo.lw import ligolw
from ligo.lw import lsctables
from ligo.lw import utils as ligolw_utils

from lal import GPSTimeNow

from ligo.scald.io import kafka

from gw.lts import utils

def parse_command_line():
	parser = utils.add_general_opts()
	parser.add_option('--preferred-event', metavar = 'func:param', default = 'max:snr', help = 'Parameter and function to use to determine preferred events in the case that multiple event messages are found for a single injection. ' +
		'Supported options are min:combined_far, max:snr, latest:msg_time, or first:msg_time')
	opts, args = parser.parse_args()

	return opts, args

def preferred_event_func(func):
	if func == 'max' or func == 'latest':
		return max
	elif func == 'min' or func == 'first':
		return min
	else:
		raise NotImplementedError

def append_sim_table(coinc_file, sim_file):
	# init a new sim inspiral table
	this_sim_table = lsctables.SimInspiralTable.get_table(sim_file)
	coinc_file.childNodes[-1].appendChild(this_sim_table)

	return coinc_file

def write_sim_file(sim, xmldoc):
	# open a new xml doc
	sim_msg = io.BytesIO()
	ligolw_elem = xmldoc.appendChild(ligolw.LIGO_LW())

	output_simtable = ligolw_elem.appendChild(lsctables.New(lsctables.SimInspiralTable))
	this_sim_table = lsctables.SimInspiralTable.get_table(sim)
	output_simtable.extend(this_sim_table)
	ligolw_utils.write_fileobj(xmldoc, sim_msg, gz = False)

	return sim_msg

def construct_event_ouput(xmldoc, event, injection, key=None):
	filename = f'coinc-{int(event["time"])}.xml' if not key else f'{key}-coinc-{int(event["time"])}.xml'

	coinctable = lsctables.CoincInspiralTable.get_table(event['coinc'])

	ligolw_utils.write_filename(xmldoc, os.path.join('coincs', filename), verbose = opts.verbose)
	coinc_msg = io.BytesIO()
	ligolw_utils.write_fileobj(xmldoc, coinc_msg, gz = False)

	output = {
		'time': coinctable[0].end_time,
		'time_ns': coinctable[0].end_time_ns,
		'snr': coinctable[0].snr,
		'far': coinctable[0].combined_far,
		'p_astro': event['p_astro'],
		'coinc': coinc_msg.getvalue().decode(),
		'latency': event['latency'],
		'onIFOs': injection['ifos']
		}

	return output

def process_events(events, injections, msgs, pipeline):
	# for each event in the event_msgs deque, find the nearest injection in inj_msgs
	# within +/- delta_t (1 second) of the event coalescence time.
	# when an association is made, remove both messages from the deques,
	# add the sim inspiral table from injection to the event's coinc xml and 
	# send a message to the testsuite.events topic for all the other jobs to consume
	events_copy = copy.copy(events)
	for event in events_copy:
		event_time = event['time']
	
		nearest_inj = utils.find_nearest_msg(injections, event_time)
	
		# if no associated injection was found, pass
		if not nearest_inj:
			continue

		inj_time = nearest_inj['time']
		sim_file = nearest_inj['sim']

		# remove the event from the deque and unpack info
		events.remove(event)
		coinc_file = event['coinc']
		this_coinc = lsctables.CoincInspiralTable.get_table(coinc_file)
		this_sngl = lsctables.SnglInspiralTable.get_table(coinc_file)
		this_coinc_event = lsctables.CoincTable.get_table(coinc_file)	
	
		time_now = int(GPSTimeNow())
		if preferred_param == 'combined_far' or preferred_param == 'snr':
			val = this_coinc.getColumnByName(preferred_param)[0]
		elif preferred_param == 'msg_time':
			val = event['msg_time']
		else:
			raise NotImplementedError

		# Note: this requires that aggregate by "latest" works the way we would hope
		if inj_time in msgs.keys():
			vals = list(msgs[inj_time].values()) + [val]
			if not val is preferred_func(vals):
				logging.debug(f'New event for injection: {inj_time}. This {preferred_param} {val} not preferred to send an update msg, continuing.')
				continue
			# wait some time before sending an update message
			if not time_now - max(msgs[inj_time].keys()) >= 10.:
				continue
			logging.debug(f'New event for injection {inj_time}. This {preferred_param} {val} is preferred, sending an update msg')
			msgs[inj_time].update({time_now: val})

		else:
			logging.debug(f'Initial event found for injection {inj_time} with {preferred_param} {val}.')
			msgs[inj_time] = {time_now: val}

		# store relevant info for missed/found table in coinc_dict_list
		coinc_dict = {}

		for attr in ("combined_far", "snr", "false_alarm_rate"):
			try:
				coinc_dict[attr] = float(this_coinc.getColumnByName(attr)[0])
			except TypeError:
				pass
		coinc_dict["end"] = float(event_time)

		for attr in ("likelihood",):
			try:
				coinc_dict[attr] = this_coinc_event.getColumnByName(attr)[0]
			except TypeError:
				pass

		for sngl_row in this_sngl:
			for attr in ("snr", "chisq", "mass1", "mass2", "spin1z", "spin2z", "coa_phase"):
				if getattr(sngl_row, attr):
					coinc_dict["%s_%s" % (sngl_row.ifo, attr)] = float(getattr(sngl_row, attr))
			if sngl_row.end:
				coinc_dict["%s_end" % sngl_row.ifo] = float(sngl_row.end)

		# proceed with sending event
		# add sim table to coinc file and write to disk
		newxmldoc = append_sim_table(coinc_file, sim_file)

		output = construct_event_ouput(newxmldoc, event, nearest_inj)

		client.write(f'{pipeline}.{tag}.testsuite.events', output)
		logging.info(f'Sent msg to: {pipeline}.{tag}.testsuite.events')
		newxmldoc.unlink()

		# send inj_table_events message
		client.write(f'{pipeline}.{tag}.testsuite.inj_table_events', [coinc_dict])
		logging.info(f'Sent msg to: {pipeline}.{tag}.testsuite.inj_table_events')

def process_stale_msgs(msgs, topic, msgs_sent, pipeline):
	# process old messages: either messages that are about to be 
	# removed from the left of the deque, or have been in the deque
	# for 2 hours, and send a message with the necessary info
	# this is necessary in the case that:
		# 1) we receive an event from the search which is not
		# associated with an injection, ie a glitch or real gw 
		# candidate.
		# 2) there is an injection for which we never receive
		# an associated event from the search. ie the injection
		# was not recovered at even the GDB far threshold.
	# FIXME dont hardcode wait time
	if msgs and ((len(msgs) == maxlen) or (float(GPSTimeNow()) - msgs[0]['time'] >= 7200.)):
		stale_msg = msgs[0]

		if topic == 'inj_events':
			logging.debug(f'{pipeline} event from time {stale_msg["time"]} to be removed from the queue - no associated injection found')

		elif topic == 'inj_stream':
			sim_inspiral = stale_msg['sim']

			if not stale_msg['time'] in msgs_sent.keys():
				logging.debug(f'Sending {pipeline} missed injection msg for injection {stale_msg["time"]}')
				newxmldoc = ligolw.Document()
				sim_msg = write_sim_file(sim_inspiral, newxmldoc)

				output = {
						'sim': sim_msg.getvalue().decode(),
						'onIFOs': stale_msg['ifos'],
				}

				client.write(f'{pipeline}.{tag}.testsuite.missed_inj', output)
				logging.info(f'Sent msg to: {pipeline}.{tag}.testsuite.missed_inj')
				newxmldoc.unlink()

def main():
	# parse options from command line
	opts, args = parse_command_line()
	
	tag = opts.tag
	topics = opts.input_topic
	preferred_func = preferred_event_func(opts.preferred_event.split(':')[0])
	preferred_param = opts.preferred_event.split(':')[1]
	
	# set up producer
	client = kafka.Client(f'kafka://{tag}@{opts.kafka_server}')
	
	# set up logging
	utils.set_up_logger(opts.verbose)
	
	# set up dir for output coincs
	try:
		os.mkdir('coincs')
	except OSError as error:
		pass
	
	# initialize data deques
	# if injections come every ~20 seconds this should correspond 
	# to keeping messages for about 3-4 minutes.
	maxlen = 10
	event_msgs = defaultdict(lambda: deque(maxlen=maxlen))
	inj_msgs = defaultdict(lambda: deque(maxlen=maxlen))
	msgs_sent = defaultdict(lambda: OrderedDict())
	
	# create a job service using cronut
	inspinjmsg_find = App('inspinjmsg_find', broker=f'kafka://{tag}_inspinjmsg_find@{opts.kafka_server}')
	
	# subscribes to inj_stream and inj_events topics
	@inspinjmsg_find.process(topics)
	def process(message): 
		mtopic = message.topic().split('.')[-1]
		mpipeline = message.topic().split('.')[0]
	
		# unpack data from the message
		if mtopic == 'inj_events':
			# parse event info
			event = json.loads(message.value())
	
			# load the coinc table
			coinc_file = utils.load_xml(event['coinc'])
			coinctable = lsctables.CoincInspiralTable.get_table(coinc_file)
	
			# get event coalescence time
			coinctime = coinctable[0].end_time + 10.**-9. * coinctable[0].end_time_ns
			logging.info(f'received {mpipeline} event with coalescence time: {coinctime}')
	
			if 'latency' in event.keys():
				latency = event['latency']
			else:
				latency = None
	
			# store event data
			event_msgs[mpipeline].append({
							'time': coinctime,
							'coinc': coinc_file,
							'p_astro': event['p_astro'],
							'latency': latency,
							'msg_time': int(GPSTimeNow())
			})
	
			process_events(event_msgs[mpipeline], copy.deepcopy(inj_msgs[mpipeline]), msgs_sent[mpipeline], pipeline = mpipeline)
			process_stale_msgs(event_msgs[mpipeline], mtopic, msgs_sent[mpipeline], pipeline = mpipeline)
	
		elif mtopic == 'inj_stream':
			# parse inj info
			injection = json.loads(message.value())
			ifos = injection['onIFOs']
	
			# load the sim table
			simfile = utils.load_xml(injection['sim'])
			simtable = lsctables.SimInspiralTable.get_table(simfile)
	
			# get injection coalescence time
			coinctime = simtable[0].geocent_end_time + 10.**-9 * simtable[0].geocent_end_time_ns
			logging.info(f'received {mpipeline} injection with coalescence time: {coinctime}')
	
			# store inj data
			inj_msgs[mpipeline].append({
							'time': coinctime,
							'sim': simfile,
							'ifos': ifos
			})
	
			process_events(event_msgs[mpipeline], copy.deepcopy(inj_msgs[mpipeline]), msgs_sent[mpipeline], pipeline = mpipeline)
			process_stale_msgs(inj_msgs[mpipeline], mtopic, msgs_sent[mpipeline], pipeline = mpipeline)
	
		else:
			# break
			logging.debug(f'Error: Found unexpected message from topic {mtopic}.')

	# start up
	logging.info('Starting up...')
	inspinjmsg_find.start()

if __name__ == '__main__':
	main()
