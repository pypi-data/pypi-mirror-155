# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dippy', 'dippy.config', 'dippy.extensions', 'dippy.labels', 'dippy.utils']

package_data = \
{'': ['*']}

install_requires = \
['bevy>=0.4.5,<0.5.0',
 'nextcord>=2.0.0-alpha.2,<3.0.0',
 'pydantic>=1.8.1,<2.0.0']

extras_require = \
{'postgres': ['psycopg2-binary>=2.8.6,<3.0.0'],
 'sqlalchemy': ['SQLAlchemy>=1.3.23,<2.0.0'],
 'yaml': ['pyyaml>=5.3.1,<6.0.0']}

setup_kwargs = {
    'name': 'dippy.bot',
    'version': '0.1.1a26',
    'description': 'A Discord bot framework built to simplify the complicated parts of bot development.',
    'long_description': 'A Discord bot framework built to simplify the complicated parts of bot development.\n',
    'author': 'Zech Zimmerman',
    'author_email': 'hi@zech.codes',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ZechCodes/Dippy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
