#!/usr/bin/env python3

from optparse import OptionParser
import logging
import json
import os
import io
import sys
import copy
import numpy
import random
from time import sleep
from collections import defaultdict, OrderedDict

from ligo.lw import ligolw
from ligo.lw import lsctables
from ligo.lw import utils as ligolw_utils
from ligo.lw.param import Param
from ligo.lw.utils.process import register_to_xmldoc
from ligo.skymap.tool import bayestar_realize_coincs
from ligo.skymap.bayestar import filter as bayestar_filter

from confluent_kafka import Producer, Consumer

import lal
from lal import GPSTimeNow, LIGOTimeGPS, GreenwichMeanSiderealTime
from lal import MSUN_SI, PC_SI
import lal.series
import lalsimulation

from ligo.scald.io import kafka

from gw.lts import utils
from gw.lts.utils import cosmology_utils as cutils
from gw.lts.utils import pastro_utils

class LIGOLWContentHandler(ligolw.LIGOLWContentHandler):
	pass

lsctables.use_in(LIGOLWContentHandler)

# define input opts
def parse_command_line():
	parser = utils.add_general_opts()
	parser.add_option('--time-offset', type = int, help = 'Time offset to shift injections by. Not used if data-source is fake-data, required otherwise.. If using mdc injections this should be non-zero number that corresponds to the time h(t) is shifted by. For gstlal injections from disk, this should be 0.')
	parser.add_option('--psd-file', metavar = 'file', help = 'Path to reference PSD file.')
	parser.add_option('--track-psd', action='store_true', default = False, help = 'Dynamically update PSD. If given, kafka-server and input-topic are required. Default is False.')
	parser.add_option('--track-segments', action='store_true', default = False, help = 'Track IFO states. If given, kafka-server and input-topic are required. Default is False.')
	parser.add_option('--ifo', action = 'append', help = 'IFOs to use. Can be given more than once.')
	parser.add_option('--far-threshold', type = float, default = 2.315e-5, help = 'Set the FAR threshold for sending coincs. Used if data-source is fake-data. Default is 2 per day.')
	parser.add_option('--inj-rate', type = float, default = 20., help = 'Rate to send injection messages in the fake-data scheme. Default is 20 seconds.')
	parser.add_option('--output-coinc', metavar = 'dir', default = 'output_files', help='the directory to output coinc files to')
	opts, args = parser.parse_args()

	return opts, args

class SendInjStream(object):
	def __init__(self, options):
		logging.info('Setting up injection stream...')

		self.verbose = options.verbose
		self.tag = options.tag
		self.datasources = options.data_source
		self.time_offset = options.time_offset
		self.ifo_name = options.ifo
		self.inj_rate = options.inj_rate
		self.far_threshold = options.far_threshold
		self.output_coinc = options.output_coinc
		self.track_segments = options.track_segments
		self.track_psd = options.track_psd
		self.send_fake_coincs = True if 'fake-data' in self.datasources else False

		### set up kafka consumer and producer
		self.producer = kafka.Client(f'kafka://{tag}@{opts.kafka_server}')
		
		if options.input_topic:
			kafka_settings = {
			'bootstrap.servers': opts.kafka_server,
			'group.id': tag,
			'message.max.bytes': 5242880 # 5 MB
		}
			self.client = Consumer(kafka_settings)
			self.client.subscribe([topic for topic in opts.input_topic])

		### set up psds and segments
		self.new_psds = {}
		self.psds = self.load_psd(options.psd_file)

		if options.track_segments:
			self.segments = defaultdict(lambda: OrderedDict())

		### additional set up for the fake data configuration
		if options.send_fake_coincs:
			self.fake_data_setup()

		# load sorted sim inspiral table
		self.simtable = self.load_sim_table(options.inj_file)

	def start(self):
		logging.info('Starting injection stream...')
		# step through sim table row by row, update sim col values as necessary,
		# send message to inj_stream, then if data-source is fake-data, 
		# generate a coinc file and send a message to events topic
		while self.simtable:
			# remove and return the oldest/first inj in the table
			thisrow = self.simtable.pop(0)
		
			if self.send_fake_coincs:
				# sleep for inj cadence
				sleep(self.inj_rate)
		
				timenow = float(GPSTimeNow())
				time_offset = timenow - thisrow.geocent_end_time
				injection_time = thisrow.geocent_end_time + time_offset
		
			else:
				timenow = float(GPSTimeNow())
				time_offset = self.time_offset
				injection_time = thisrow.geocent_end_time + time_offset
		
				# if the injection is already passed, skip it
				if timenow - (injection_time) >= 5 * 60.:
					logging.debug('Skipping old injection')
					continue
		
				# sleep until its close to the next inj time
				time_to_sleep = (injection_time) - timenow
				if time_to_sleep > 0.:
					logging.debug('Sleeping until next injection...')
					sleep(time_to_sleep)
		
			logging.debug(f'Processing injection at coa tim: {injection_time}')

			# track segments and psds
			if self.track_segments:
				self.segments_tracker(injection_time)
			elif self.track_psd:
				new_psd_msgs, _ = self.pull_dq_messages()
		
			# once we have the state vector segments that we need,
			# update the psds just once
			if self.track_psd and new_psd_msgs:
				self.track_psds(new_psd_msgs)

			# proceed to generate the correct sim row and send
			# an output message kafka
			outxml, output_simtable = self.new_sim_xml()
			output_row = copy.copy(thisrow)

			# if time offset is nonzero, shift the times, longitude
			# and re-calculate the inj snrs
			if time_offset:
				output_row = self.shift_times(output_row, time_offset)
				inj_snrs = self.calc_inj_snrs(output_row)

				# add inj snrs to appropriate cols in output_row 
				output_row.alpha4 = inj_snrs['H1']
				output_row.alpha5 = inj_snrs['L1']
				output_row.alpha6 = inj_snrs['V1']

				logging.debug(f"SNRs: H1: {output_row.alpha4} | L1: {output_row.alpha5} | V1: {output_row.alpha6}")

			# construct sim table
			output_simtable.append(output_row)
			outxml.childNodes[-1].appendChild(output_simtable)

			sim_msg = io.BytesIO()
			ligolw_utils.write_fileobj(outxml, sim_msg, gz = False)

			# get state vector at time of this injection
			# in fake data configuration, lets just assume all IFOs
			# are always on
			onIFOs = []
			if self.send_fake_coincs:
				onIFOs = ['H1', 'L1', 'V1']
			# FIXME: we are assuming that no state info for a given time
			# means that the IFO was off. This is a bad idea and we should
			# really fix it to make sure that we receive explicit 0 states 
			# at times when the IFOs actually were off.
			if self.track_segments:
				for ifo, states in self.segments.items():
					try:
						ifo_on = states[injection_time]
						if ifo_on:
							onIFOs.append(ifo)
					except KeyError:
						near_times = []
						for time, state in states.items():
							if injection_time - 0.5 < time < injection_time + 0.5:
								near_times.append((time, state))

						ifo_on = near_times and all(s[1] for s in near_times)
						if ifo_on:
							onIFOs.append(ifo)
			logging.debug(f'on IFOs: {onIFOs}')

			# construct output json packet
			output = {
					'sim': sim_msg.getvalue().decode(),
					'onIFOs': (',').join(onIFOs)
			}

			# output msgs to kafka
			for datasource in self.datasources:
				self.producer.write(f'{datasource}.{self.tag}.inj_stream', output)
				logging.info(f'Sent msg to: {datasource}.{self.tag}.inj_stream')

			if not self.send_fake_coincs:
				outxml.unlink()
				continue

			# otherwise, proceed to send the coinc message
			trigger = copy.copy(output_row)
			outxml.unlink()

			coincfar = self.snr_to_far_map([trigger.alpha4, trigger.alpha5, trigger.alpha6])

			# propduce a fake coinc if the far passes the threshold
			if coincfar < self.far_threshold:
				logging.debug('Sending a coinc trigger...')
				resp = self.produce_coinc_output(trigger)
			else:
				logging.debug(f'Coinc FAR {coincfar:e} above threshold to send message')

		logging.info('Sent all injections. Exiting ...')

	def load_psd(self, file):
		xmldoc = ligolw_utils.load_filename(file, contenthandler = lal.series.PSDContentHandler)
		return lal.series.read_psd_xmldoc(xmldoc, root_name=None)

	def fake_data_setup(self):
		self.detectors = [lalsimulation.DetectorPrefixToLALDetector(ifo) for ifo in self.ifo_name]
		self.responses = [det.response for det in detectors]
		self.locations = [det.location for det in detectors]
		
		# the interpolated object below will be used for SNR time series simulation
		self.psds_dict = {key: bayestar_filter.InterpolatedPSD(bayestar_filter.abscissa(psd), psd.data.data)
			for key, psd in self.psds.items() if psd is not None}
		self.psds_interp = [psds_dict[ifo] for ifo in self.ifo_name]

		### compute distributions required for pastro calculation
		self.p_x_c = pastro_utils.p_x_c(bns=(1.22, .06), nsbh=(6.27, 1.84), bbh=(42.98, 8.11))
		self.p_c = pastro_utils.p_c(p_x_c, N_events={"Terrestrial": 0, "BNS": 60800, "NSBH": 48400, "BBH": 60800})

	def load_sim_table(self, file):
		xmldoc = ligolw_utils.load_filename(file, contenthandler = LIGOLWContentHandler)
		simtable = lsctables.SimInspiralTable.get_table(xmldoc)

		return simtable.sort(key = lambda row: row.geocent_end_time + 10.**-9. * row.geocent_end_time_ns)

	def segments_tracker(self, injection_time, max_retries = 10):
		have_states = {ifo: False for ifo in self.ifo_name}
	
		tries = 0
		while not all(have_states.values()) and tries < max_retries:
		       for ifo in self.ifo_name:
		       	# either we have a state corresponding to this injection time
		       	# or we have later states (for now assuming no state = IFO off)
		       	have_states[ifo] = self.segments[ifo] and (injection_time in self.segments[ifo].keys() or next(reversed(self.segments[ifo])) > injection_time)
		
		       	if have_states[ifo]:
		       		# move on to check the next ifo
		       		continue
		       	else:
		       		# sleep for the difference in time between the latest state
		       		# and this injection so that the ll_dq job can catch up
		       		if self.segments[ifo] and next(reversed(self.segments[ifo])) - injection_time > 0:
		       			sleep(next(reversed(self.segments[ifo])) - injection_time)
		
		       		# pull and store new messages and try again
		       		new_psd_msgs, new_segs = self.pull_dq_messages()
		       		self.new_psds.update(new_psd_msgs)
		
		       		store_segments(new_segs)
	
		       		tries += 1
		       		break
	
	def store_segments(self, new_segs):
		for ifo in new_segs.keys():
			for time, states in sorted(new_segs[ifo].items()):
				# for each time, we can receive states from each job.
				# take the max over the recored state from each job,
				# ie if at least one job reports that the data was on 
				# at this time, assume it was really on.
				self.segments[ifo].update({time: int(max(states))})
			while len(self.segments[ifo].keys()) >= 500.:
				self.segments[ifo].popitem(last=False)

	def pull_dq_messages(self, num_messages=10000, timeout=0.3):
		psds = {}
		statevectorsegments = defaultdict(lambda: {})
		msgs = self.client.consume(num_messages=num_messages, timeout=0.2)
		for msg in sorted(msgs, key = self.sortfunc, reverse = True):
			if msg and not msg.error():
				pipeline, tag, ifo, topic = self.parse_dq_topic(msg.topic())

				if topic.endswith("psd"):
					psd = json.loads(msg.value())
					psds.setdefault(ifo, psd)
	
				elif topic.endswith("statevectorsegments"):
					value = json.loads(msg.value())
					time = value['time']
					state = value['data']
					for t, s in zip(time, state):
						# if we're getting segs from each job, there will be duplicates.
						# append each state to a list for a given time
						statevectorsegments[ifo].setdefault(t, []).append(s)
	
		return psds, statevectorsegments

	def parse_dq_topic(self, topic):
		pipeline, tag, topic = topic.split('.')
		ifo, topic = topic.split('_')

		return pipeline, tag, ifo, topic

	def track_psds(self, new_psds):
		for ifo, data in new_psds.items():
			# parse psd data
			x = numpy.array(data['freq'])
			y = abs(numpy.array(data['asd']))**2.
	
			# make sure they are the same length
			if len(y) != len(x):
				x = x[:len(y)]
	
			# remove nans
			psd_data = numpy.array([])
			frequency = numpy.array([])
			for f, p in zip(x, y):
				if not numpy.isnan(p):
					psd_data = numpy.append(psd_data, p)
					frequency = numpy.append(frequency, f)
	
			# update psds dict with interpolated psds
			new_psd = lal.CreateREAL8FrequencySeries('new_psd', None, min(frequency), data['deltaF'], 's strain^2', len(psd_data))
			new_psd.data.data = psd_data
			self.psds.update({ifo: new_psd})
	
			self.psds_dict.update({ifo: bayestar_filter.InterpolatedPSD(frequency, psd_data)})
			logging.debug(f'Updated {ifo} PSD.')
	
		self.psds_interp = [self.psds_dict[ifo] for ifo in self.psds.keys()]

	def sortfunc(self, m):
		return m.timestamp()

	def new_sim_xml(self):
		# open a new xml doc
		xml = ligolw.Document()
		xml.appendChild(ligolw.LIGO_LW())
	
		# write a sim inspiral table with a single row corresponding to this injection
		simtable = lsctables.New(lsctables.SimInspiralTable)
		return xml, simtable

	def shift_times(self, row, time_offset):
		# fix gpstimes and RA
		row.geocent_end_time = int(row.geocent_end_time + time_offset)
		row.h_end_time = row.h_end_time + time_offset
		row.l_end_time = row.l_end_time + time_offset
		row.v_end_time = row.v_end_time + time_offset
	
		gmst0 = GreenwichMeanSiderealTime(LIGOTimeGPS(row.geocent_end_time + row.geocent_end_time_ns * 10.**-9.))
		gmst = GreenwichMeanSiderealTime(LIGOTimeGPS(row.geocent_end_time + row.geocent_end_time_ns * 10.**-9. + time_offset))
		dgmst = gmst - gmst0
		row.longitude = row.longitude + dgmst
	
		return row

	def calc_inj_snrs(self, inj):
		snr = dict.fromkeys(self.ifo_name, 0.0)
	
		injtime = inj.geocent_end_time
		f_min = inj.f_lower
		approximant = lalsimulation.GetApproximantFromString(str(inj.waveform))
		sample_rate = 16384.0
		f_max = 1600.
	
		h_plus, h_cross = lalsimulation.SimInspiralTD(
			m1 = inj.mass1*lal.MSUN_SI,
			m2 = inj.mass2*lal.MSUN_SI,
			S1x = inj.spin1x,
			S1y = inj.spin1y,
			S1z = inj.spin1z,
			S2x = inj.spin2x,
			S2y = inj.spin2y,
			S2z = inj.spin2z,
			distance = inj.distance*1e6*lal.PC_SI,
			inclination = inj.inclination,
			phiRef = inj.coa_phase,
			longAscNodes = 0.0,
			eccentricity = 0.0,
			meanPerAno = 0.0,
			deltaT = 1.0 / sample_rate,
			f_min = f_min,
			f_ref = 0.0,
			LALparams = None,
			approximant = approximant
		)
	
		h_plus.epoch += injtime
		h_cross.epoch += injtime
	
		# Compute strain in each detector. If one detector wasn't on, snr will be set to zero.
		for instrument in snr:
			if instrument not in self.psds.keys():
				continue
			h = lalsimulation.SimDetectorStrainREAL8TimeSeries(h_plus, h_cross, inj.longitude, inj.latitude, inj.polarization, lalsimulation.DetectorPrefixToLALDetector(instrument))
			snr[instrument] = lalsimulation.MeasureSNR(h, psds[instrument], f_min, f_max)
	
		return snr

	def snr_to_far_map(self, snrs):
		# this is set so that a network SNR 7 event (H1 SNR = L1 SNR = 4.) is recovered with FAR < 2/day
		return 6 * 10**-4. * numpy.exp(- (numpy.sqrt(numpy.linalg.norm([snr for snr in snrs if snr > 4.])))**2. / 2.)

	def produce_coinc_output(self, trigger, key=None):
		# build coinc xml doc, calculate p_astro, and produce message
		newxmldoc = self.build_coinc_xml(trigger)
		if not newxmldoc:
			return False
	
		coinctable = lsctables.CoincInspiralTable.get_table(newxmldoc)
		coincsnr = coinctable[0].snr
	
		p_astro = self.get_pastro(newxmldoc, coincsnr)
	
		output = self.construct_event_ouput(newxmldoc, p_astro, filekey=key)
	
		# send coinc message to events topic
		logging.info(f"network SNR: {output['snr']} | FAR: {output['far']}")
	
		self.producer.write(f'fake-data.{self.tag}.inj_events', output)
		logging.info(f'Sent msg to: fake-data.{tag}.inj_events')
		newxmldoc.unlink()
	
		return True

	def build_coinc_xml(self, row):
	
		# instantiate relevant lsctables objects
		newxmldoc = ligolw.Document()
		ligolw_elem = newxmldoc.appendChild(ligolw.LIGO_LW())
		new_process_table = ligolw_elem.appendChild(lsctables.New(lsctables.ProcessTable, columns = utils.all_process_rows))
		new_sngl_inspiral_table = ligolw_elem.appendChild(lsctables.New(lsctables.SnglInspiralTable, columns = utils.all_sngl_rows))
		new_coinc_inspiral_table = ligolw_elem.appendChild(lsctables.New(lsctables.CoincInspiralTable, columns = utils.all_coinc_rows))
		new_coinc_event_table = ligolw_elem.appendChild(lsctables.New(lsctables.CoincTable))
		new_coinc_map_table = ligolw_elem.appendChild(lsctables.New(lsctables.CoincMapTable))
	
		# simulate SNR time series using interpolated psd object
		# measurement_error is set as gaussian but one can switch to no noise by measurement_error="zero-noise"
		bayestar_sim_list = bayestar_realize_coincs.simulate(seed=None, sim_inspiral=row, psds=self.psds_interp, responses=self.responses, locations=self.locations, measurement_error="gaussian-noise", f_low=20, f_high=2048)
	
		# get mass parameters
		mass1 = max(numpy.random.normal(loc=row.mass1, scale=1.), 1.1)
		mass2 = max(numpy.random.normal(loc=row.mass2, scale=1.), mass1)
		mchirp, eta = self.mc_eta_from_m1_m2(mass1, mass2)
	
		snrs = defaultdict(lambda: 0)
		coincsnr = None
	
		# populate process table
		process_row_dict = {k:0 for k in utils.all_process_rows}
		process_row_dict.update({"process_id": 0,
					"program": "gstlal_inspiral", #FIXME
					"comment": ""
					})
		new_process_table.extend([lsctables.ProcessTable.RowType(**process_row_dict)])
	
		# populate sngl table, coinc map table, and SNR timeseriess 
		for event_id, (ifo, (horizon, abs_snr, arg_snr, toa, snr_series)) in enumerate(zip(self.ifo_name, bayestar_sim_list)):
			sngl_row_dict = {k:0 for k in utils.all_sngl_rows}
	
			sngl_row_dict.update({
					"process_id": 0,
					"event_id": event_id,
					"end": toa,
					"mchirp": mchirp,
					"mass1": mass1,
					"mass2": mass2,
					"eta": eta,
					"ifo": ifo,
					"snr": abs_snr,
					"coa_phase": arg_snr
					})
	
			# add to the sngl inspiral table
			new_sngl_inspiral_table.extend([lsctables.SnglInspiralTable.RowType(**sngl_row_dict)])
			snrs[ifo] = abs_snr
	
			coinc_map_row_dict = {"coinc_event_id": 0,
								"event_id": event_id,
								"table_name": "sngl_inspiral",
								}
	
			# add to the coinc map table
			new_coinc_map_table.extend([lsctables.CoincMapTable.RowType(**coinc_map_row_dict)])
	
			# add SNR time series as array objects
			elem = lal.series.build_COMPLEX8TimeSeries(snr_series)
			elem.appendChild(
				Param.from_pyvalue('event_id', event_id))
			ligolw_elem.appendChild(elem)
	
		# calculate coinc SNR, only proceed if above 4
		coincsnr = numpy.linalg.norm([snr for snr in snrs.values() if snr > 4])
		if not coincsnr:
			logging.debug(f'Coinc SNR {coincsnr} too low to send a message.')
			return None
	
		# populate coinc inspiral table
		coinc_row_dict = {col:0 for col in utils.all_coinc_rows}
		coincendtime = row.geocent_end_time
		coincendtimens = row.geocent_end_time_ns
		coinc_row_dict.update({
					"coinc_event_id": 0,
					"snr": coincsnr,
					"mass": row.mass1 + row.mass2,
					"mchirp": row.mchirp,
					"end_time": coincendtime,
					"end_time_ns": coincendtimens,
					"combined_far": coincfar,
					})
		new_coinc_inspiral_table.extend([lsctables.CoincInspiralTable.RowType(**coinc_row_dict)])
	
		# populate coinc event table
		coinc_event_row_dict = {col:0 for col in utils.all_coinc_event_rows}
		coinc_event_row_dict.update({
					"coinc_def_id": 0,
					"process_id": 0,
					"time_slide_id": 0,
					"instruments": "H1,L1,V1",
					"numevents": len(new_sngl_inspiral_table)
					})
		new_coinc_event_table.extend([lsctables.CoincTable.RowType(**coinc_event_row_dict)])
	
		# add psd frequeny series
		lal.series.make_psd_xmldoc(self.psds, ligolw_elem)
	
		return newxmldoc

	def mc_eta_from_m1_m2(self, m1, m2):
		mc = (m1 * m2)**(3./5.) / (m1 + m2)**(1./5.)
		eta = (m1 * m2) / (m1 + m2)**2.
	
		return mc, eta

	def get_pastro(self, xmldoc, rankstat):
		coinctable = lsctables.CoincInspiralTable.get_table(xmldoc)
	
		mchirp = coinctable[0].mchirp
	
		return pastro_utils.p_astro(mchirp, rankstat, p_x_c, p_c)
	
	def construct_event_ouput(self, xmldoc, p_astro, filekey=None):
		coinctable = lsctables.CoincInspiralTable.get_table(xmldoc)
		time = coinctable[0].end_time
	
		# write coinc file to disk
		file = f'fake_coinc-{int(time)}.xml' if not filekey else f'{filekey}-fake_coinc-{int(time)}.xml'
		ligolw_utils.write_filename(xmldoc, os.path.join(self.output_coinc, file), verbose = self.verbose)
	
		coinc_msg = io.BytesIO()
		ligolw_utils.write_fileobj(xmldoc, coinc_msg, gz = False)
	
		# create json packet
		output = {
			'time': time,
			'time_ns': coinctable[0].end_time_ns,
			'snr': coinctable[0].snr,
			'far': coinctable[0].combined_far,
			'p_astro': json.dumps(p_astro),
			'coinc': coinc_msg.getvalue().decode(),
		}
		return output

def main():
	### parse command line
	opts, args = parse_command_line()

	if opts.track_psd or opts.track_segments:
		if not getattr(opts, 'kafka_server'):
			raise ValueError(f'Must specify --kafka-server when --track-psd or --track-segments is set.')
		if not getattr(opts, 'input_topic'):
			raise ValueError(f'Must specify at least one --input-topic when --track-psd or --track-segments is set.')
	
	try:
		os.mkdir(opts.output_coinc)
	except OSError as error:
		pass
	
	### set up logger
	logger = utils.set_up_logger(opts.verbose)
	
	### initialize and set up
	send_inj_stream = SendInjStream(opts)

	### start the stream
	send_inj_stream.start()

if __name__ == '__main__':
	main()
