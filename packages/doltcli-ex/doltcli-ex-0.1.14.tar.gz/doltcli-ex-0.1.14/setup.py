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
    'version': '0.1.14',
    'description': 'Enhanced Dolt CLI',
    'long_description': "# doltcli-ex\n\n## Introduction\n\nAn Enhanced CLI for dolt.The official doltcli only provides git-like operations inside Dolt among the SQL tables,but not the files.So,to be more friendly,doltcli-ex provides commands to simplify the io operations and dolt operations.\n\n### Commands\n\nThe *scripts* provides convenient Python scripts to add and remove data files in dolt. The installation will create executables automatically.\n\n- *doltadd* : Import the dataset file as SQL table or upload some kind of special files(README.md,LICENSE.md) in Dolt and then add it into Dolt's stage.\n\n- *doltrm* : Remove a table or some kind of special files in Dolt.\n\n\n\n## Installation\n\n### From pip\n\n``` sh\npip install doltcli-ex\n```\n\n\n### From source\n\n``` sh\npip install git+https://github.com/yuiant/doltcli-ex.git\n```\n\n## Contribution\n\n### Formatting Code\n\nTo ensure the codebase complies with a style guide, please use [flake8](https://github.com/PyCQA/flake8), [black](https://github.com/psf/black) and [isort](https://github.com/PyCQA/isort) tools to format and check codebase for compliance with PEP8.\n",
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
