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
{'console_scripts': ['get-metars = get_metars.__main__:app']}

setup_kwargs = {
    'name': 'get-metars',
    'version': '0.3.1',
    'description': "Simple command line tool to download METAR's and TAF's for a given station and store them in text files.",
    'long_description': "# get-metars\n\nSimple command line tool to download METAR's and TAF's for a given station and\nstore them in text files.\n\n## Requirements\n\nThis package requires:\n\n* [Python ^3.7][python-home]\n\n[python-home]: https://www.python.org\n\nPython because it was developed on that version.\n\n## Installation\n\nFor install only run this command from your terminal\n\n```\npip install get-metars\n```\n\n### Update\n\nUpdate with `pip` adding the option --upgrade\n\n```\npip install --upgrade get-metars\n```\n\n## Examples\n\nThe data are downloaded from [Ogimet.com][ogimet-home], so be nice and don't saturate\nthe server. This site only accepts requests of data of 31 days or less at a time.\n\n[ogimet-home]: http://ogimet.com\n\nTo download data for a specific month (i.e. january 2022) of JFK INT. Airport only run \n\n```\nget-metars kjfk --init 2022-01-01\n```\n\nThe program will understand that you want all data of the month.\n\nIf you need only the METAR's run\n\n```\nget-metars kjfk --init 2022-01-01 --type SA\n```\n\nwhere `SA` means `METAR` type of aeronautical report. Type `get-metars --help` to see all\nthe available options.\n\nIf you need a specific time of period you need to give the initial and final datetimes,\nas follows\n\n```\nget-metars kjfk --init 2021-12-05T01:00:00 --final 2021-12-10T22:30:00 --type SP\n```\n\nwhere `SP` means `SPECI` type of aeronautical reports.\n\nTo standarize the reports for TAF-VER verification program add the flag `--sanitize` or `-s`.\nTo make the program store the reports in one line add the flag `--one-line` or `-o`.\nBy default, reports are written to the file with the datetime prefix with format `%Y%m%d%H%M`. If you\nwant to remove that prefix add the flag `--no-datetime-prefix`.\n\nSo that's it. Simple no?\nHave a happy coding :D",
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
