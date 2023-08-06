# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['p360_export',
 'p360_export.config',
 'p360_export.data',
 'p360_export.exceptions',
 'p360_export.export',
 'p360_export.extra_data',
 'p360_export.query',
 'p360_export.utils']

package_data = \
{'': ['*'], 'p360_export': ['_config/*']}

install_requires = \
['Salesforce-FuelSDK>=1.3.0,<2.0.0',
 'console-bundle==0.5.1',
 'daipe-core>=1.2,<2.0',
 'databricks-bundle>=1.4.5,<2.0.0',
 'facebook-business>=13.0.0,<14.0.0',
 'google-ads>=16.0.0,<17.0.0',
 'jsonschema>=4.4.0,<5.0.0',
 'paramiko>=2.11.0,<3.0.0',
 'pyarrow==4.0.0',
 'pyfony-bundles==0.4.4',
 'pyfony-core>=0.8.0,<0.9.0']

entry_points = \
{'pyfony.bundle': ['create = p360_export.P360Export:P360Export']}

setup_kwargs = {
    'name': 'p360-export',
    'version': '1.0.0',
    'description': 'Persona360 data export',
    'long_description': '# p360-export\n\nPersona360 exporters.\n',
    'author': 'Datasentics',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.10,<4.0.0',
}


setup(**setup_kwargs)
