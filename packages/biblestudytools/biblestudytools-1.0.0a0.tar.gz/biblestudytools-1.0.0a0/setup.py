# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['biblestudytools', 'biblestudytools.bible']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'click>=8.1.3,<9.0.0',
 'requests>=2.28.0,<3.0.0']

entry_points = \
{'console_scripts': ['biblestudytools = biblestudytools.__main__:main']}

setup_kwargs = {
    'name': 'biblestudytools',
    'version': '1.0.0a0',
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
