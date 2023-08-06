# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dooit', 'dooit.ui', 'dooit.ui.events', 'dooit.ui.widgets', 'dooit.utils']

package_data = \
{'': ['*']}

install_requires = \
['pyperclip>=1.8.2,<2.0.0', 'textual>=0.1.17,<0.2.0']

entry_points = \
{'console_scripts': ['dooit = dooit.__init__:main']}

setup_kwargs = {
    'name': 'dooit',
    'version': '0.1.0',
    'description': 'A TUI todo manager',
    'long_description': None,
    'author': 'kraanzu',
    'author_email': 'kraanzu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
