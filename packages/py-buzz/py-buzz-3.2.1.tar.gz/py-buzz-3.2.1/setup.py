# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['buzz']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

setup_kwargs = {
    'name': 'py-buzz',
    'version': '3.2.1',
    'description': '"That\'s not flying, it\'s falling with style": Exceptions with extras',
    'long_description': ".. image::  https://badge.fury.io/py/py-buzz.svg\n   :target: https://badge.fury.io/py/py-buzz\n   :alt:    Latest Version\n\n.. image::  https://travis-ci.org/dusktreader/py-buzz.svg?branch=integration\n   :target: https://travis-ci.org/dusktreader/py-buzz\n   :alt:    Build Status\n\n.. image::  https://readthedocs.org/projects/py-buzz/badge/?version=latest\n   :target: http://py-buzz.readthedocs.io/en/latest/?badge=latest\n   :alt:    Documentation Status\n\n*********\n py-buzz\n*********\n\n------------------------------------------------------------------\nThat's not flying, it's falling with style: Exceptions with extras\n------------------------------------------------------------------\n\npy-buzz supplies some useful tools to use with python exceptions as well\nas a base Buzz exception class that includes them as classmethods.\n\npy-buzz is fully equipped with exception tools that are written over and over\nagain in python projects such as:\n\n* checking conditions and raising errors on failure (``require_conditon``)\n* checking that values are defined and raising errors if not (``enforce_defined``)\n* catching exceptions wrapping them in clearer exception types with better error\n  messages (``handle_errors``)\n* checking many conditions and reporting which ones failed\n  (``check_expressions``)\n\nBuzz can be used as a stand-alone exception class, but it is best used as a\nbass class for custom exceptions within a project. This allows the user to\nfocus on creating a set of Exceptions that provide complete coverage for issues\nwithin their application without having to re-write convenience functions\nthemselves.\n\nSuper-quick Start\n-----------------\n - requirements: `python3.6+`\n - install through pip: `$ pip install py-buzz`\n - minimal usage example: `examples/with_buzz_class.py <https://github.com/dusktreader/py-buzz/tree/master/examples/with_buzz_class.py>`_\n\nDocumentation\n-------------\n\nThe complete documentation can be found at the\n`py-buzz home page <http://py-buzz.readthedocs.io>`_\n",
    'author': 'Tucker Beck',
    'author_email': 'tucker.beck@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
