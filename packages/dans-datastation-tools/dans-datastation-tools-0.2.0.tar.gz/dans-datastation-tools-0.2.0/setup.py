# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datastation', 'datastation.scripts']

package_data = \
{'': ['*']}

install_requires = \
['dicttoxml>=1.7.4,<2.0.0',
 'lxml>=4.8.0,<5.0.0',
 'pyYAML>=6.0,<7.0',
 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['convert-dataset-metadatafiles = '
                     'datastation.scripts.convert_dataset_metadatafiles:main',
                     'delete-drafts = datastation.scripts.delete_datasets:main',
                     'delete-role-assignments = '
                     'datastation.scripts.delete_roleassignments:main',
                     'oai-harvest = datastation.scripts.oai_harvest:main',
                     'publish-datasets = '
                     'datastation.scripts.publish_datasets:main',
                     'reindex-datasets = '
                     'datastation.scripts.reindex_datasets:main',
                     'replace-metadata-field-values = '
                     'datastation.scripts.replace_metadata_field_values:main',
                     'retrieve-dataset-metadata = '
                     'datastation.scripts.retrieve_dataset_metadata:main',
                     'retrieve-dataset-pids = '
                     'datastation.scripts.retrieve_dataset_pids:main',
                     'unlock-datasets = '
                     'datastation.scripts.unlock_datasets:main',
                     'update-datacite-records = '
                     'datastation.scripts.update_datacite-records:main']}

setup_kwargs = {
    'name': 'dans-datastation-tools',
    'version': '0.2.0',
    'description': 'Command line utilities for Data Station application management',
    'long_description': None,
    'author': 'DANS-KNAW',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
