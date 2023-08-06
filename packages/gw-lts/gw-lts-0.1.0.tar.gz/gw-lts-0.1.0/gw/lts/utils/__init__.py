import logging
from io import StringIO, BytesIO
from ligo.lw import ligolw
from ligo.lw import lsctables
from ligo.lw import utils as ligolw_utils

from ligo.segments import segment
from ligo.scald.utils import floor_div

import yaml
from yaml.loader import SafeLoader

from optparse import OptionParser

class LIGOLWContentHandler(ligolw.LIGOLWContentHandler):
    pass

lsctables.use_in(LIGOLWContentHandler)

all_sngl_rows = ("process:process_id", "ifo", "search", "channel", "end_time", "end_time_ns", "end_time_gmst", "impulse_time", "impulse_time_ns", "template_duration", "event_duration", "amplitude", "eff_distance", "coa_phase", "mass1", "mass2", "mchirp", "mtotal", "eta", "kappa", "chi", "tau0", "tau2", "tau3", "tau4", "tau5", "ttotal", "psi0", "psi3", "alpha", "alpha1", "alpha2", "alpha3", "alpha4", "alpha5", "alpha6", "beta", "f_final", "snr", "chisq", "chisq_dof", "bank_chisq", "bank_chisq_dof", "cont_chisq", "cont_chisq_dof", "sigmasq", "rsqveto_duration", "Gamma0", "Gamma1", "Gamma2", "Gamma3", "Gamma4", "Gamma5", "Gamma6", "Gamma7", "Gamma8", "Gamma9", "spin1x", "spin1y", "spin1z", "spin2x", "spin2y", "spin2z", "event_id")

all_coinc_rows = ("coinc_event:coinc_event_id", "combined_far", "end_time", "end_time_ns", "false_alarm_rate", "ifos", "mass", "mchirp", "minimum_duration", "snr")

all_coinc_event_rows = ("coinc_definer:coinc_def_id", "coinc_event_id", "instruments", "likelihood", "nevents", "process:process_id", "time_slide:time_slide_id")

all_coinc_map_rows = {"coinc_event:coinc_event_id", "event_id", "table_name"}

all_process_rows = ("comment", "cvs_entry_time", "cvs_repository", "domain", "end_time", "ifos", "is_online", "jobid", "node" , "process_id", "program", "start_time", "unix_procid", "username", "version")


def add_general_opts():
	parser = OptionParser()
	parser.add_option('--data-source', metavar = 'string', action='append', help = 'Source of test suite data. Options: fake-data, gstlal, mbta, pycbc.')
	parser.add_option('--tag', help = 'The tag used to uniquely identify the analysis you wish to process metrics from. Used as Kafka group ID.')
	parser.add_option('--kafka-server', metavar = 'string', help = 'Sets the url for the kafka broker.')
	parser.add_option('--analysis-dir', metavar='path', help = '')
	parser.add_option('--inj-file', metavar='file', help='')
	parser.add_option('--input-topic', metavar = 'string', action='append', help = 'The Kafka topic(s) to subscribe to.')
	parser.add_option('--group', metavar='string', default = 'gracedb-playground', help = 'GraceDb group to use. Valid options are gracedb, gracedb-playground, and gracedb-test.')
	parser.add_option('--verbose', default=False, action="store_true", help = 'Be verbose.')

	return parser

def set_up_logger(verbose):
	logging.getLogger()
	if verbose:
		log_level = logging.DEBUG
	else:
		log_level = logging.INFO

	handler = logging.StreamHandler()
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)
	logging.getLogger('').addHandler(handler)
	logging.getLogger('').setLevel(log_level)

def load_xml(f, gz=False):
	if isinstance(f, str):
		f = BytesIO(f.encode("utf-8"))
	xmldoc = ligolw_utils.load_fileobj(f, contenthandler = LIGOLWContentHandler, gz=gz)

	return xmldoc

def load_filename(f, gz=True):
	xmldoc = ligolw_utils.load_filename(f, contenthandler = LIGOLWContentHandler, gz=gz)

	return xmldoc

def event_window(t):
	"""
	returns the event window representing the event
	"""
	dt = 0.2
	return segment(floor_div(t - dt, 0.5), floor_div(t + dt, 0.5) + 0.5)

def get_ifos(sngltable):
	ifos = ''
	for row in sngltable:
		if not row.ifo in ifos:
			ifos += str(row.ifo)

	return ifos

def source_tag(simtable):
	mass1 = simtable[0].mass1
	mass2 = simtable[0].mass2
	cutoff = 3 # minimum BH mass

	if mass1 < cutoff and mass2 < cutoff: source = 'BNS'
	elif mass1 >= cutoff and mass2 >= cutoff: source = 'BBH'
	else: source = 'NSBH'
	return source

def parse_msg_key(message):
	try:
		key = message.key().decode("utf-8")
	except AttributeError:
		key = None
	return key

def find_nearest_msg(msgs, t):
	# get injections close to the event end time
	delta = 1.0

	# construct a list of tuples (msg, Delta_t) where Delta_t is the difference in time
	# between this msg and the input time, sort by Delta_t, and take the first element
	# in the list which corresponds to the msg closest to the input time
	nearest_msg = None
	try:
		near_msgs = list((msg, abs(msg['time'] - t)) for msg in msgs if t - delta <= msg['time'] <= t + delta)
		if near_msgs:
			nearest_msg = sorted(near_msgs, key = lambda x: x[1])[0][0]

			logging.debug(f'Time to search for: {t} | Nearest msg time: {nearest_msg["time"]}')
	except Exception as e:
		logging.debug(f'Error: {e}')
	return nearest_msg

def decisive_snr(sngl_snrs, ifos):
	ifos = ifos.split(',')
	sngl_snrs = [sngl_snrs[ifo] for ifo in ifos]

	# if no ifos, assume all were off
	if len(ifos) == 0:
		return 0
	# for single time, use the most sensitive IFO
	elif len(ifos) == 1:
		return sorted(sngl_snrs, reverse=True)[0]
	# for coinc time, use the SNR of the second most sensitive IFO
	elif len(ifos) >= 2:
		return sorted(sngl_snrs, reverse=True)[1]

def eta_from_m1_m2(m1, m2):
	# symmetric mass ratio from component masses
	m1 = float(m1)
	m2 = float(m2)
	return (m1 * m2) / (m1 + m2)**2.

def mchirp_from_m1_m2(m1, m2):
	# chirp mass from component masses
	m1 = float(m1)
	m2 = float(m2)
	return (m1 * m2)**(3./5.) / (m1 + m2)**(1./5.)

