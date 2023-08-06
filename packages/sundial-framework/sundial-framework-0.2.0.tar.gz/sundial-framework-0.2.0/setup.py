# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sundial']

package_data = \
{'': ['*']}

install_requires = \
['markdown!=3.3.5',
 'matplotlib',
 'numpy',
 'pandas',
 'plotly',
 'scikit-learn',
 'tensorflow>=2.4.4,!=2.5.0,!=2.5.1,!=2.6.0']

setup_kwargs = {
    'name': 'sundial-framework',
    'version': '0.2.0',
    'description': 'The Sundial timeseries model data framework.',
    'long_description': None,
    'author': 'Gavin Bell',
    'author_email': 'gavin.bell@optimeering.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
