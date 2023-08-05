# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mikro', 'mikro.api', 'mikro.composition', 'mikro.fakts', 'mikro.links']

package_data = \
{'': ['*']}

install_requires = \
['dask>=2022.2.1,<2023.0.0',
 'fakts==0.2.4',
 'herre>=0.2.4,<0.3.0',
 'pandas>=1.3.4,<2.0.0',
 'pyarrow>=6.0.1,<7.0.0',
 'rath>=0.2.4,<0.3.0',
 's3fs>=2022.2.0,<2023.0.0',
 'websockets>=10.2,<11.0',
 'xarray>=2022.3.0,<2023.0.0',
 'zarr>=2.11.1,<3.0.0']

extras_require = \
{'complete:python_version >= "3.9"': ['turms>=0.2.3,<0.3.0'],
 'turms:python_version >= "3.9"': ['turms>=0.2.3,<0.3.0']}

setup_kwargs = {
    'name': 'mikro',
    'version': '0.2.4',
    'description': 'images for arnheim',
    'long_description': None,
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
