# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lite_term_system_stats']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.5,<0.5.0', 'psutil>=5.9.1,<6.0.0']

setup_kwargs = {
    'name': 'lite-term-system-stats',
    'version': '0.1.23',
    'description': '',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
