# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['admin_reorder']

package_data = \
{'': ['*'],
 'admin_reorder': ['static/css/*',
                   'static/img/*',
                   'static/js/*',
                   'templates/admin-reorder/*']}

install_requires = \
['Django>=3.2']

setup_kwargs = {
    'name': 'django-admin-model-reorder',
    'version': '0.1.0',
    'description': 'Fork of django-admin-model-reorder (courtesy of Misbah Razzaque); intended to keep up with the updates of Django and python',
    'long_description': None,
    'author': 'fsecada01',
    'author_email': 'francis.secada@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
