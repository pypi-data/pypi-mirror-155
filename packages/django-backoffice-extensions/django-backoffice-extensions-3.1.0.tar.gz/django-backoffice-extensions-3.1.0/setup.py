# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['backoffice_extensions',
 'backoffice_extensions.forms',
 'backoffice_extensions.templatetags']

package_data = \
{'': ['*'],
 'backoffice_extensions': ['locale/en/LC_MESSAGES/*',
                           'locale/es/LC_MESSAGES/*',
                           'templates/backoffice/*',
                           'templates/backoffice/bases/*',
                           'templates/backoffice/partials/*',
                           'templates/backoffice/widgets/*']}

install_requires = \
['django-model-utils>=4.0.0,<5.0.0',
 'django>=4.0.0,<5.0.0',
 'pytest-cov>=2.10.0,<3.0.0']

setup_kwargs = {
    'name': 'django-backoffice-extensions',
    'version': '3.1.0',
    'description': 'A set of views, tools and helpers to create a backoffice using Django.',
    'long_description': 'Django Backoffice Extensions\n============================\n\nA set of views, tools and helpers to create a backoffice using Django.',
    'author': 'Marcos Gabarda',
    'author_email': 'marcos@dekalabs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Dekalabs/django-backoffice-extensions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
