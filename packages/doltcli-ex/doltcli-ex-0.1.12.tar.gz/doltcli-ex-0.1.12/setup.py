# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doltcli_ex', 'doltcli_ex.scripts']

package_data = \
{'': ['*']}

install_requires = \
['doltpy==2.0.13', 'pandas']

entry_points = \
{'console_scripts': ['doltadd = doltcli_ex.scripts.add:main',
                     'doltrm = doltcli_ex.scripts.rm:main']}

setup_kwargs = {
    'name': 'doltcli-ex',
    'version': '0.1.12',
    'description': 'Enhanced Dolt CLI',
    'long_description': None,
    'author': 'yuiant',
    'author_email': 'gyuiant@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yuiant/doltcli-ex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
