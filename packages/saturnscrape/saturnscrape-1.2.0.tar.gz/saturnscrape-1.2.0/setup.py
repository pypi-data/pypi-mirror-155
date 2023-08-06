# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['saturnscrape']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT[crypto]>=2.3.0,<3.0.0',
 'aiofiles>=0.8.0,<0.9.0',
 'aiohttp>=3.8.1,<4.0.0',
 'arrow>=0.11,<0.15',
 'ics>=0.7,<0.8',
 'pytz>=2022.1,<2023.0',
 'tzlocal>=4.2,<5.0',
 'vobject>=0.9.6,<0.10.0']

entry_points = \
{'console_scripts': ['saturnscrape = saturnscrape:__main__.main']}

setup_kwargs = {
    'name': 'saturnscrape',
    'version': '1.2.0',
    'description': 'Scrapes information from https://saturn.live, a collaborate school scheduling system.',
    'long_description': '# saturnscrape\n\nScrapes information from https://saturn.live, a collaborate school scheduling system.\n\nCurrently, this Python package only aims to support the scheduling and members of a school.\n\n## Example\n\n```python\nfrom asyncio import run\nfrom typing import cast\n\nfrom saturnscrape import *\n\n\nasync def runner():\n    client = SaturnLiveClient("jwt", "refresh token")\n    print(cast(FullStudent, await client.get_student("me")).phone_number)\n    await client.close()\n    \n\nrun(runner())\n```\n\nAlso provides a simple command line tool for downloading the schedule and members of a school to vCard and vCalendar/iCalendar files.\n',
    'author': 'Parker Wahle',
    'author_email': 'parkeredwardwahle2017@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/regulad/saturnscrape',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
