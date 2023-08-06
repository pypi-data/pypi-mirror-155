# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['photonbend',
 'photonbend.core',
 'photonbend.exceptions',
 'photonbend.lens',
 'photonbend.projections',
 'photonbend.scripts',
 'photonbend.scripts.commands',
 'photonbend.utils']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.1,<10.0.0',
 'click>=8.0.4,<9.0.0',
 'numba>=0.55.1,<0.56.0',
 'numpy>=1.18,<1.22',
 'scipy>=1.8.0,<2.0.0']

entry_points = \
{'console_scripts': ['photonbend = photonbend.scripts.main:main']}

setup_kwargs = {
    'name': 'photonbend',
    'version': '0.1.1',
    'description': 'Photonbend allows one to convert photos between different sorts of lenses, rotate photos and make panoramas.',
    'long_description': None,
    'author': 'Edson Moreira',
    'author_email': 'w.moreirae@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
