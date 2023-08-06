#!/usr/bin/env python3

from optparse import OptionParser
import os
import sys
import json
import logging
import math
import atexit

from collections import defaultdict, deque

from confluent_kafka import Producer
from cronut import App
from cronut.utils import uriparse

from ligo.lw import lsctables
from ligo.lw import utils as ligolw_utils
from ligo.lw.utils.process import register_to_xmldoc

from lal import GPSTimeNow

from ligo.scald.io import kafka

from gw.lts import utils
from gw.lts.utils import cosmology_utils as cutils

def parse_command_line():
	parser = utils.add_general_opts()
	parser.add_option('--far-threshold', default=2.314e-5,  help = 'far threshold for missed vs found injections. Default is 2 per day.')
	parser.add_option('--calculate-injected-vt', action='store_true', help='If the injection file doesnt already have an injected VT calculated and stored in Process Params Table , calculate it here on the fly.' + 
			'In this case, max_redshift is required.')
	parser.add_option('--max-redshift', metavar = 'SOURCE:float', action = 'append', help='The max redshift used when generating the injection set.' +
			'Required if --calculate-injected-vt is set. Can be given multiple times.')
	parser.add_option('--bootstrap-vt', action='store_true', default=False, help = 'Whether to load counts for previous found injections from the injection set.' + 
			'This is used to calculate a cumulative VT even if the job is re-started.')
	opts, args = parser.parse_args()

	return opts, args

def write_counts_to_disk(num_found, exp_num_found, filename):
	xmldoc = utils.load_filename(filename)
	process_params_table = lsctables.ProcessParamsTable.get_table(xmldoc)

	process_params_table, new_vt_rows = process_update(num_found, process_params_table, rowname = 'cumulative-vt')
	process_params_table, new_exp_vt_rows = process_update(exp_num_found, process_params_table, rowname = 'cumulative-exp-vt')

	new_vt_rows.update(new_exp_vt_rows)
	if new_vt_rows:
		register_to_xmldoc(xmldoc, program = 'vt', paramdict = new_vt_rows, comment = 'Cumulative VT')

	ligolw_utils.write_filename(xmldoc, filename, verbose = True)

def process_update(dict, table, rowname):
	new_rows = {}
	for pipeline in dict.keys():
		for key, data in dict[pipeline].items():
			logging.debug(f'At shutdown: {pipeline} {key} {rowname} last time: {data[-1][0]} | last count: {data[-1][1]}')
			updated = 0
			# if the row already exists, update its value
			for r in table:
				if str(r.param).strip('--') == f'{rowname}:{pipeline}-{key}':
					logging.debug(f'found row to update: {str(r.param)}...')
					r.value = f'{data[-1][0]}:{data[-1][1]}'
					updated += 1
			# otherwise, add a new row
			if not updated:
				logging.debug('no row to update, writing a new row...')
				new_rows[f'{rowname}:{pipeline}-{key}'] =  f'{data[-1][0]}:{data[-1][1]}'

	return table, new_rows

def parse_vt_from_process(row):
	params = str(row.param).split(':')[1]
	pipeline, source = params.split('-')
	time, count = str(row.value).split(':')

	return pipeline, source, time, count

def injected_VT(pptable):
	# parse process params table
	ppdict = {}
	for r in pptable:
		try:
			ppdict.setdefault(str(r.param).strip('--'), []).append(float(r.value))
		except:
			ppdict.setdefault(str(r.param).strip('--'), []).append(r.value)

	# First get total number of injections
	if 'accept' in ppdict and 'reject' in ppdict:
		num_total_injections = sum(ppdict['accept']) + sum(ppdict['reject'])
	elif 'total-generated' in ppdict:
		num_total_injections = sum(ppdict['total-generated'])
	else:
		raise Exception('Could not find total number of attempted injections in file, exiting')

	# try to calculate VT myself
	if num_total_injections and opts.calculate_injected_vt and opts.max_redshift:
		try:
			omega = cutils.get_cosmo_params()
			gps_start = ppdict['gps-start'][0]
			gps_end = ppdict['gps-end'][0]

			VT = {}
			for z in opts.max_redshift:
				source = z.split(':')[0].upper()
				val = float(z.split(':')[1])
			
				VT.update({source: cutils.surveyed_spacetime_volume(gps_start, gps_end, val, omega)})
				logging.debug(f'{source} VT: {VT[source]}')
			VT.update({'VT': sum(VT[source] for source in VT.keys())})

			return VT, num_total_injections
		except:
			 raise Exception('Could not calculate the injected VT, exiting')

	# try getting VT from the injection file
	else:
		try:
			VT = {}
			for item in ['bns-vt', 'nsbh-vt', 'bbh-vt', 'VT']:
				if item in ppdict:
					key = item.split('-')[0].upper()
					VT.setdefault(key, sum(ppdict[item]))
					logging.debug(f'{key} VT: {sum(ppdict[item])}')

			return VT, num_total_injections

		except:
			 raise Exception('Could not get VT from the Process Params Table, exiting')

def main():
	opts, args = parse_command_line()
	
	tag = opts.tag
	far_threshold = float(opts.far_threshold)
	pipelines = [x.split('.')[0] for x in opts.input_topic]
	
	# set up producer
	client = kafka.Client(f'kafka://{tag}@{opts.kafka_server}')
	
	# set up logging
	utils.set_up_logger(opts.verbose)
	
	# load and parse injection file for injected VT and total injections
	inj_file = utils.load_filename(opts.inj_file, gz=True)
	ProcessParamsTable = lsctables.ProcessParamsTable.get_table(inj_file)
	
	inj_VT, total_inj = injected_VT(ProcessParamsTable)
	
	if not inj_VT:
		raise Exception('Injected VT dict is empty, exiting')
	
	# initialize dicts to store data
	num_found = defaultdict(lambda: defaultdict(lambda: deque(maxlen=300)))
	expected_num_found = defaultdict(lambda: defaultdict(lambda: deque(maxlen=300)))
	output = defaultdict(lambda: {'time': [], 'data': []})
	
	# init num found to 0 for every ifo combination
	startup_time = float(GPSTimeNow())
	
	# add previous found injection counts first
	if opts.bootstrap_vt:
		for r in ProcessParamsTable:
			if 'cumulative-vt' in str(r.param):
				pipeline, source, time, count = parse_vt_from_process(r)
				num_found[pipeline][source].append((float(time), float(count)))
				logging.debug(f'Bootstrapping found injections for {pipeline} {source} from time: {time}, count: {count}')
	
			if 'cumulative-exp-vt' in str(r.param):
				pipeline, source, time, count = parse_vt_from_process(r)
				expected_num_found[pipeline][source].append((float(time), float(count)))
				logging.debug(f'Bootstrapping expected found injections for {pipeline} {source} from time: {time}, count: {count}')
	
	# for any pipelines or sources that didn't have a previously recorded value
	# in the injection file, start the count from zero
	for pipeline in pipelines:
		for key in inj_VT:
			if not num_found[pipeline][key]:
				if opts.bootstrap_vt:
					logging.debug(f'No {pipeline} {key} counts found to bootstrap. Starting count from 0.')
				num_found[pipeline][key].append((startup_time, 0))
			if not expected_num_found[pipeline][key]:
				if opts.bootstrap_vt:
					logging.debug(f'No {pipeline} {key} expected counts found to bootstrap. Starting count from 0.')
				expected_num_found[pipeline][key].append((startup_time, 0))
	
	# create a job service using cronut
	sensitive_vt = App('sensitive_vt', broker=f'kafka://{tag}_vt@{opts.kafka_server}')
	
	# subscribes to a topic
	@sensitive_vt.process(opts.input_topic)
	def process(message): 
		mtopic = message.topic().split('.')[-1]
		mpipeline = message.topic().split('.')[0]
		mkey = utils.parse_msg_key(message)
		logging.debug(f'Read message from {mpipeline} {mtopic}')
	
		# dont process old messages or noninjection events
		event = json.loads(message.value())
		time = event['time'] + event['time_ns'] * 10**-9.
		if time > startup_time and not mkey == 'noninj':
			# parse event info
			coinc_file = utils.load_xml(event['coinc'])
			simtable = lsctables.SimInspiralTable.get_table(coinc_file)
	
			far = event['far']
			snr = event['snr']
	
			source = utils.source_tag(simtable)
	
			# try calculating source specific VTs, otherwise just calculalte overall VT
			if source in inj_VT:
				key = source
			else:
				key = 'VT'
	
			# calculate decisive SNR and count expected number of found injections
			ifos = event['onIFOs']
			inj_snrs = defaultdict(lambda: None)
			inj_snrs['H1'] = simtable[0].alpha4
			inj_snrs['L1'] = simtable[0].alpha5
			inj_snrs['V1'] = simtable[0].alpha6
	
			decisive_snr = utils.decisive_snr(inj_snrs, ifos)
	
			if decisive_snr:
				prev_exp_found = expected_num_found[mpipeline][key][-1][1]
				this_expected_found = prev_exp_found + 1 if decisive_snr >= 8. else prev_exp_found
				expected_num_found[mpipeline][key].append((time, this_expected_found))
	
			# Count the actual  number of found injections so far
			prev_num_found = num_found[mpipeline][key][-1][1]
			this_num_found = prev_num_found + 1 if far < far_threshold else prev_num_found
			num_found[mpipeline][key].append((time, this_num_found))
	
			# Calculate the current and expected VT
			if decisive_snr:
				expected_VT = (this_expected_found / total_inj) * inj_VT[key]
				output['exp_vt'] = {
					'time': [ time ],
					'data': [ expected_VT ]
				}
			VT = (this_num_found / total_inj) * inj_VT[key]
	
			output['vt'] = {
				'time': [ time ],
				'data': [ VT ]
			}
	
			# Calculate the current and expected sensitive volume (scaled for time)
			# divide the VT by the total elapsed time
			dt = abs(time - startup_time) / 60. / 60. / 24. / 365.25 # yr
			if decisive_snr:
				expected_V = expected_VT / dt
				output['exp_sensitive_vol'] = {
					'time': [ time ],
					'data': [ expected_V ]
				}
			V = VT / dt
	
			output['sensitive_vol'] = {
				'time': [ time ],
				'data': [ V ]
			}
	
	
			# Calculate the current and expected range, assuming V is a sphere
			if decisive_snr:
				expected_R = (expected_V / (4. * math.pi / 3.))**(1./3.)
				output['exp_range'] = {
					'time': [ time ],
					'data': [ expected_R ]
				}
			R = (V / (4. * math.pi / 3.))**(1./3.)
	
			output['range'] = {
				'time': [ time ], 
				'data': [ R ]
			}
	
			if decisive_snr:
				logging.debug(f'{mpipeline}: {source} expec. VT: {expected_VT} Gpc3 yr | expc. V: {expected_V} Gpc3 | expec. range: {expected_R} Gpc')
			logging.info(f'{mpipeline}: {source} current VT: {VT} Gpc3 yr | V: {V} Gpc3 | range: {R} Gpc')
			for topic in output:
				client.write(f'{mpipeline}.{tag}.testsuite.{topic}', output[topic], tags = source)
				logging.info(f'Sent msg to: {mpipeline}.{tag}.testsuite.{topic}')

	# at exit, writ counts to disk
	atexit.register(write_counts_to_disk, num_found, expected_num_found, opts.inj_file)
	
	# start up
	logging.info('Starting up...')
	sensitive_vt.start()

if __name__ == '__main__':
	main()
