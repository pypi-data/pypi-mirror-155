# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moosee']

package_data = \
{'': ['*']}

install_requires = \
['keyboard>=0.13.5,<0.14.0',
 'opencv-python>=4.6.0,<5.0.0',
 'pynput>=1.7.6,<2.0.0']

entry_points = \
{'console_scripts': ['moosee = moosee.__main__:start']}

setup_kwargs = {
    'name': 'moosee',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'wvlab',
    'author_email': 'wvlab@protonmail.com',
    'maintainer': 'wvlab',
    'maintainer_email': 'wvlab@protonmail.com',
    'url': 'https://github.com/wvlab/moosee',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
