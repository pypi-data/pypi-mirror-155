# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['example_template_foundation']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.1b3', 'requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'example-template-foundation',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Anustup Das',
    'author_email': 'anustup@mediadistillery.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
