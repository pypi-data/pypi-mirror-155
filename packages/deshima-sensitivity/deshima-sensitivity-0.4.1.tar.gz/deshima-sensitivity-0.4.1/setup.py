# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deshima_sensitivity']

package_data = \
{'': ['*'], 'deshima_sensitivity': ['data/*']}

install_requires = \
['jupyter-io>=0.2,<0.3',
 'lmfit>=1.0,<2.0',
 'matplotlib>=3.2,<4.0',
 'scipy>=1.4,<2.0']

extras_require = \
{':python_full_version >= "3.7.1" and python_version < "3.8"': ['numpy>=1.20,<1.22',
                                                                'pandas>=1.3,<1.4'],
 ':python_version >= "3.8" and python_version < "3.11"': ['numpy>=1.20,<2.0',
                                                          'pandas>=1.3,<2.0']}

setup_kwargs = {
    'name': 'deshima-sensitivity',
    'version': '0.4.1',
    'description': 'Sensitivity calculator for DESHIMA-type spectrometers',
    'long_description': '# deshima-sensitivity\n\n[![Release](https://img.shields.io/pypi/v/deshima-sensitivity?label=Release&color=cornflowerblue&style=flat-square)](https://pypi.org/pypi/deshima-sensitivity/)\n[![Python](https://img.shields.io/pypi/pyversions/deshima-sensitivity?label=Python&color=cornflowerblue&style=flat-square)](https://pypi.org/pypi/deshima-sensitivity/)\n[![Downloads](https://img.shields.io/pypi/dm/deshima-sensitivity?label=Downloads&color=cornflowerblue&style=flat-square)](https://pepy.tech/project/deshima-sensitivity)\n[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.3966839-cornflowerblue?style=flat-square)](https://doi.org/10.5281/zenodo.3966839)\n[![Tests](https://img.shields.io/github/workflow/status/deshima-dev/deshima-sensitivity/Tests?label=Tests&style=flat-square)](https://github.com/deshima-dev/deshima-sensitivity/actions/tests.yml)\n\nSensitivity calculator for DESHIMA-type spectrometers\n\n## Overview\n\ndeshima-sensitivity is a Python package which enables to calculate observation sensitivity of DESHIMA-type spectrometers.\nCurrently it is mainly used to estimate the observation sensitivity of [DESHIMA](http://deshima.ewi.tudelft.nl) and its successors.\n\nAn online Jupyter notebook is available for DESHIMA collaborators to calculate the sensitivity and the mapping speed of the DESHIMA 2.0 by themselves.\nClick the budge below to open it in [Google colaboratory](http://colab.research.google.com/) (a Google account is necessary to re-run it).\n\n### Stable version (recommended)\n\n[![open stable version in colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/deshima-dev/deshima-sensitivity/blob/v0.4.1/sensitivity.ipynb)\n\n### Latest version\n\n[![open latest version in colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/deshima-dev/deshima-sensitivity/blob/main/sensitivity.ipynb)\n\nIn the case of running it in a local Python environment, please follow the requirements and the installation guide below.\n\n## Requirements\n\n- **Python:** 3.7, 3.8, or 3.9 (tested by the authors)\n- **Dependencies:** See [pyproject.toml](https://github.com/deshima-dev/deshima-sensitivity/blob/main/pyproject.toml)\n\n## Installation\n\n```shell\n$ pip install deshima-sensitivity\n```\n\n## Development environment\n\nThe following steps can create a standalone development environment (VS Code + Python).\n\n1. Install [VS Code] and [Docker Desktop], and launch them\n1. Install the [Remote Containers] extension to VS Code\n1. Clone this repository\n1. Open the repository by VS Code\n1. Choose `Reopen in Container` from the [Command Palette]\n\n[Command Palette]: https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette\n[Docker Desktop]: https://www.docker.com/products/docker-desktop\n[Remote Containers]: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers\n[VS Code]: https://code.visualstudio.com\n\n',
    'author': 'Akira Endo',
    'author_email': 'a.endo@tudelft.nl',
    'maintainer': 'Akio Taniguchi',
    'maintainer_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'url': 'https://github.com/deshima-dev/deshima-sensitivity',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
