# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ussa1976']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0',
 'netCDF4>=1.5.7',
 'numpy>=1.22',
 'scipy>=1.6.3',
 'xarray>=0.18.2,<2022.4.0']

entry_points = \
{'console_scripts': ['ussa1976 = ussa1976.__main__:main']}

setup_kwargs = {
    'name': 'ussa1976',
    'version': '0.3.0',
    'description': 'Ussa1976',
    'long_description': "USSA1976\n========\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/ussa1976.svg\n   :target: https://pypi.org/project/ussa1976/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/ussa1976\n   :target: https://pypi.org/project/ussa1976\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/ussa1976\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/ussa1976/latest.svg?label=Read%20the%20Docs\n   :target: https://ussa1976.readthedocs.io/\n   :alt: Read the documentation at https://ussa1976.readthedocs.io/\n.. |Tests| image:: https://github.com/nollety/ussa1976/workflows/Tests/badge.svg\n   :target: https://github.com/nollety/ussa1976/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/nollety/ussa1976/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/nollety/ussa1976\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* TODO\n\n\nRequirements\n------------\n\n* Python 3.8+\n\n\nInstallation\n------------\n\nYou can install *USSA1976* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install ussa1976\n\n\nUsage\n-----\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*USSA1976* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/nollety/ussa1976/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://ussa1976.readthedocs.io/en/latest/usage.html\n",
    'author': 'Yvan Nollet',
    'author_email': 'yvan.nollet@rayference.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nollety/ussa1976',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
