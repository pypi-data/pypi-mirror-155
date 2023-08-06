# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dask_janelia']

package_data = \
{'': ['*']}

install_requires = \
['dask-jobqueue>=0.7.1,<0.8.0', 'distributed>=2022.6.0,<2023.0.0']

setup_kwargs = {
    'name': 'dask-janelia',
    'version': '0.1.5',
    'description': 'Simple dask distributed deployment for the Janelia Research Campus compute cluster.',
    'long_description': None,
    'author': 'Davis Vann Bennett',
    'author_email': 'davis.v.bennett@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
