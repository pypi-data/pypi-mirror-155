# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nima']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'matplotlib>=2.0.0',
 'numpy>=1.16',
 'pandas>=0.19',
 'scikit-image>=0.14',
 'scipy>=0.18.1',
 'tifffile>2019.7.2']

entry_points = \
{'console_scripts': ['bias = nima.__main__:bias', 'nima = nima.__main__:main']}

setup_kwargs = {
    'name': 'nima',
    'version': '0.5.4',
    'description': 'Numerical IMage Analyses.',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/nima.svg)][pypi status]\n[![Python Version](https://img.shields.io/pypi/pyversions/nima)][pypi status]\n[![image](https://github.com/darosio/nima/actions/workflows/tests.yml/badge.svg)](https://github.com/darosio/nima/actions/workflows/tests.yml)\n[![image](https://codecov.io/gh/darosio/nima/branch/main/graph/badge.svg?token=OR0LUZUJUR)](https://codecov.io/gh/darosio/nima)\n\n[pypi status]: https://pypi.org/project/nima/\n\nA library and a cli to help image analyses based on scipy.ndimage and\nscikit-image.\n\n# Features\n\n-   easy dark and flat correction\n-   automatic cell segmentation\n-   easy ratio analyses\n\n# Installation\n\n:\n\n\tpyenv virtualenv 3.6.13 nima-0.3.1-py36\n\tpoetry install\n\tpip install .\n\nOptionally:\n\n\tpython -m ipykernel install \\--user \\--name=\\"nima0.3.1\\"\n\n\n# Usage\n\nTo use nima in a project:\n\n    from nima import nima\n\nSee documentation for the `nima` command line.\n\n## Description\n\nA longer description of your project goes here\\...\n\n## Note\n\npoetry rocks? development my idea is to use global flake8 and black and\nno need to track linting and safety in poetry. KISS.\n\npyenv activate nima-... poetry install pre-commit install before next\nfirst commit: pre-commit run \\--all-files\n\npyenv activare nima-0.2 poetry install pip install . so it is not\ninstalled in development mode and this version will persist to updates.\n\n## todo\n\n- restore sane complexity value (< 21).\n',
    'author': 'daniele arosio',
    'author_email': 'daniele.arosio@cnr.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/darosio/nima/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
