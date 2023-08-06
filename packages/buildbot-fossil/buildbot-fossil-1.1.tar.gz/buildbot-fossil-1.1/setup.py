# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['buildbot_fossil', 'buildbot_fossil.test']

package_data = \
{'': ['*']}

install_requires = \
['buildbot>=3,<4', 'treq>=20']

entry_points = \
{'buildbot.changes': ['FossilPoller = buildbot_fossil.changes:FossilPoller'],
 'buildbot.steps': ['Fossil = buildbot_fossil.steps:Fossil']}

setup_kwargs = {
    'name': 'buildbot-fossil',
    'version': '1.1',
    'description': 'Fossil version control plugin for Buildbot',
    'long_description': '# Fossil plugin for Buildbot\n\n[![Documentation Status](https://readthedocs.org/projects/buildbot-fossil/badge/?version=latest)](https://buildbot-fossil.readthedocs.io/en/latest/?badge=latest)\n\n[Fossil](https://fossil-scm.org/) is a software configuration management system.\nThis [Buildbot](https://buildbot.net) plugin provides two classes to use in\n`master.cfg`:\n\n1. `changes.FossilPoller` polls a Fossil HTTP server for new checkins.\n\n2. `steps.Fossil` checks out a source revision from a Fossil repo before a build.\n\n',
    'author': 'Jakob Stoklund Olesen',
    'author_email': 'stoklund@2pi.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stoklund/buildbot-fossil',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
