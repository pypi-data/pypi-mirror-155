# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wagtail_spa_integration', 'wagtail_spa_integration.templatetags']

package_data = \
{'': ['*'], 'wagtail_spa_integration': ['templates/wagtailadmin/pages/*']}

install_requires = \
['Django>=3.2.0',
 'django-filter>=2.3.0,<3.0.0',
 'wagtail-headless-preview>=0.2,<0.3',
 'wagtail>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'wagtail-spa-integration',
    'version': '2.1.4',
    'description': 'Tools for using Wagtail API with JavaScript single page apps',
    'long_description': None,
    'author': 'David Burke',
    'author_email': 'david@burkesoftware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
