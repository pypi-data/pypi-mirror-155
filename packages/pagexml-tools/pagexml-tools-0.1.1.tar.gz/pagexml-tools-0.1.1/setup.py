# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pagexml', 'pagexml.model']

package_data = \
{'': ['*']}

install_requires = \
['icecream>=2.1.2,<3.0.0',
 'numpy>=1.22.3,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'scipy>=1.7.0,<2.0.0',
 'xmltodict>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['version = poetry_scripts:version']}

setup_kwargs = {
    'name': 'pagexml-tools',
    'version': '0.1.1',
    'description': 'Utility functions for reading PageXML files',
    'long_description': '# pagexml-tools\n\n[![GitHub Actions](https://github.com/knaw-huc/pagexml/workflows/tests/badge.svg)](https://github.com/knaw-huc/pagexml/actions)\n[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)\n[![Documentation Status](https://readthedocs.org/projects/pagexml/badge/?version=latest)](https://pagexml.readthedocs.io/en/latest/?badge=latest)\n[![PyPI](https://img.shields.io/pypi/v/pagexml-tools)](https://pypi.org/project/pagexml-tools/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pagexml-tools)](https://pypi.org/project/pagexml-tools/)\n\nUtility functions for reading [PageXML](https://www.primaresearch.org/tools/PAGELibraries) files\n\n## installing\n\n### using poetry\n\n```commandline\npoetry add pagexml-tools\n```\n\n### using pip\n\n```commandline\npip install pagexml-tools\n```\n\n----\n\n[USAGE](https://pagexml.readthedocs.io/en/latest/) |\n[CONTRIBUTING](CONTRIBUTING.md) |\n[LICENSE](LICENSE)\n',
    'author': 'Marijn Koolen',
    'author_email': 'marijn.koolen@huygens.knaw.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/knaw-huc/pagexml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
