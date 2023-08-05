# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apis_import_project', 'apis_import_project.migrations']

package_data = \
{'': ['*'],
 'apis_import_project': ['static/apis_import_project/css/*',
                         'static/apis_import_project/js/*',
                         'templates/element_templates/*',
                         'templates/pages/*',
                         'templates/section_templates/*']}

setup_kwargs = {
    'name': 'apis-import-project',
    'version': '0.3.5',
    'description': 'Generic Django-App for APIS-instances to support importing new data manually with a streamlined workflow and some automation.',
    'long_description': None,
    'author': 'Gregor Pirgie',
    'author_email': 'gregor.pirgie@oeaw.ac.at',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
