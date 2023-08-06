import os
import setuptools
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text()

install_requires = [
	'confluent-kafka>=1.7.0',
	'pyyaml',
	'python-ligo-lw==1.7.1',
	'lalsuite==6.82',
	'cronut>=0.1.0',
	'ligo-scald>=0.8.0',
	'ligo.skymap',
	'igwn-alert',
	'hop-client',
]

setuptools.setup(
	name = 'gw-lts',
	description = 'Gravitational Wave Low-Latency Test Suite',
	long_description = long_description,
	long_description_content_type='text/markdown',
	version = '0.1.0',
	author = 'Becca Ewing',
	author_email = 'rebecca.ewing@ligo.org',
	url = 'https://git.ligo.org/rebecca.ewing/gw-lts.git',
	license = 'MIT',

	packages = ['gw', 'gw.lts', 'gw.lts.utils'],

	entry_points = {
		'console_scripts': [
			'igwn-alert-listener=gw.lts.igwn_alert_listener:main',
			'send-inj-stream=gw.lts.send_inj_stream:main',
			'inspinjmsg-find=gw.lts.inspinjmsg_find:main',
			'inj-missed-found=gw.lts.inj_missed_found:main',
			'vt=gw.lts.vt:main',
			'snr-consistency=gw.lts.snr_consistency:main',
			'inj-accuracy=gw.lts.inj_accuracy:main',
			'p-astro=gw.lts.p_astro:main',
			'skymap=gw.lts.skymap:main',
			'latency=gw.lts.latency:main',
			'likelihood=gw.lts.likelihood:main',
		],
	},

	data_files = [('etc', ['etc/example_config.yml', 'etc/example_fake_data_config.yml']),
		('injections', ['injections/fake_data_injections.xml.gz'])
	],

	python_requires = '>=3.6.*',
	install_requires = install_requires,
	zip_safe = False,

	classifiers = [
		'Development Status :: 3 - Alpha',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Intended Audience :: Science/Research',
		'Natural Language :: English',
	],

)
