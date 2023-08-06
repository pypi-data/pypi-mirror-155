# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geowrangler']

package_data = \
{'': ['*']}

install_requires = \
['fastcore>=1.4,<2.0',
 'geopandas>=0.10,<0.11',
 'numpy>=1.21,<2.0',
 'pandas>=1.2,<2.0']

setup_kwargs = {
    'name': 'geowrangler',
    'version': '0.1.0.dev0',
    'description': 'Tools for dealing with geospatial data',
    'long_description': None,
    'author': 'Thinking Machines',
    'author_email': 'geowrangler@thinkingmachin.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
