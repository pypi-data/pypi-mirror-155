# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['argsense',
 'argsense.click_vendor',
 'argsense.parser',
 'argsense.style',
 'argsense.style.color_scheme']

package_data = \
{'': ['*']}

install_requires = \
['rich']

setup_kwargs = {
    'name': 'argsense',
    'version': '0.1.2',
    'description': 'New command line interface based on Python Rich library.',
    'long_description': '# Argsense CLI\n\n**argsense** is a command line interface made with Python.\n\n![](.assets/eg01/20220615143658.jpg)\n\n![](.assets/eg01/20220615143730.jpg)\n\n![](.assets/eg01/20220615143751.jpg)\n\n![](.assets/eg01/20220615143817.jpg)\n\n## Usage\n\n> Currently this section is under construction.\n\n> Please check the folder ./examples for your reference.\n',
    'author': 'Likianta',
    'author_email': 'likianta@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/likianta/argsense-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
