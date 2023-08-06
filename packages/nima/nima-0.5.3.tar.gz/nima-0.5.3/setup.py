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
    'version': '0.5.3',
    'description': 'Numerical IMage Analyses.',
    'long_description': '.. image:: https://github.com/darosio/nima/actions/workflows/tests.yml/badge.svg\n   :target: https://github.com/darosio/nima/actions/workflows/tests.yml\n\n.. image:: https://codecov.io/gh/darosio/nima/branch/main/graph/badge.svg?token=OR0LUZUJUR\n   :target: https://codecov.io/gh/darosio/nima\n\n.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n\nA library and a cli to help image analysis based on scipy.ndimage and scikit-image.\n\nFeatures\n--------\n- easy dark and flat correction\n- automatic cell segmentation\n- easy ratio analyses\n\n\nInstallation\n------------\n\n    $ pyenv virtualenv 3.6.13 nima-0.3.1-py36\n    $ poetry install\n    $ pip install .\n\nOptionally:\n    $ python -m ipykernel install --user --name="nima0.3.1"\n\n    # Jedi not working\n    %config Completer.use_jedi = False\n    for python >= 3.7 should not be needed because ipython >= 7.20 will be used.\n\n\nUsage\n-----\n\nTo use nima in a project::\n\n    from nima import nima\n\n\nSee documentation.\n\n\nDescription\n===========\n\nA longer description of your project goes here...\n\n\nNote\n====\n\npoetry rocks?\ndevelopment\nmy idea is to use global flake8 and black and no need to track linting and safety in poetry. KISS.\n\npyenv activate nima-…\npoetry install\npre-commit install\nbefore next first commit:\npre-commit run --all-files\n\npyenv activare nima-0.2\npoetry install\npip install .\nso it is not installed in development mode and this version will persist to updates.\n\ntodo\n====\n- restore sane complexity value\n- CI and static typing\n',
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
