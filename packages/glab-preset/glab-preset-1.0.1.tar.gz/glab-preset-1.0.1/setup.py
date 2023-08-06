# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['glab_preset']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'python-gitlab>=3.5.0,<4.0.0']

entry_points = \
{'console_scripts': ['glab_preset = glab_preset.main:cli']}

setup_kwargs = {
    'name': 'glab-preset',
    'version': '1.0.1',
    'description': 'Gitlab preset tool.',
    'long_description': None,
    'author': 'afeiship',
    'author_email': '1290657123@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
