# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['get_metars']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'html5lib>=1.1,<2.0',
 'pydantic>=1.9.1,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['tafver = get_metars.__main__:get_metars']}

setup_kwargs = {
    'name': 'get-metars',
    'version': '0.1.0',
    'description': "Simple command line tool to download METAR's and TAF's for a given station and store them in text files.",
    'long_description': None,
    'author': 'diego-garro',
    'author_email': 'diego.garromolina@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/diego-garro/tafver-metars',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
