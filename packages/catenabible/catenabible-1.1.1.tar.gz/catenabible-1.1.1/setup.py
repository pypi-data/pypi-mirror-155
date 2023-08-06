# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['catenabible']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'click>=8.1.3,<9.0.0',
 'requests>=2.28.0,<3.0.0']

entry_points = \
{'console_scripts': ['catena = catena.__main__:catena']}

setup_kwargs = {
    'name': 'catenabible',
    'version': '1.1.1',
    'description': '',
    'long_description': None,
    'author': 'numbergazing',
    'author_email': 'hello@numbergazing.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
