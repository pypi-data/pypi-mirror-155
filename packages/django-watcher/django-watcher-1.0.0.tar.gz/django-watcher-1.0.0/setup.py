# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_watcher']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'django-watcher',
    'version': '1.0.0',
    'description': 'Django Data Watcher is a library that will make easier to create/mantain side-effects of data operations in your django models.',
    'long_description': None,
    'author': 'Vinta Serviços e Soluções Tecnológicas LTDA',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.8,<4.0.0',
}


setup(**setup_kwargs)
