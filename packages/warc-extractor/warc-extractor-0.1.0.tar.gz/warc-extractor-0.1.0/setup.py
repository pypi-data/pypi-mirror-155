# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['warc_extractor']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['warc-extractor = warc_extractor.warc_extractor:main']}

setup_kwargs = {
    'name': 'warc-extractor',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
