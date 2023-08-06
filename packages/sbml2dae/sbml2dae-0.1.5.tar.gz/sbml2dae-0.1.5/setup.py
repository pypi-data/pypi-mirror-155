# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sbml2dae']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.0,<9.0.0', 'python-libsbml==5.19.5']

entry_points = \
{'console_scripts': ['sbml2dae = sbml2dae.cli:main']}

setup_kwargs = {
    'name': 'sbml2dae',
    'version': '0.1.5',
    'description': 'A customizable SBML to Matlab parser',
    'long_description': '# SBML2dae: a customizable SBML to Matlab parser\n\n[![GitHub Actions][github-actions-badge]](https://github.com/sb2cl/sbml2dae/actions)\n[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n\n[github-actions-badge]: https://github.com/sb2cl/sbml2dae/workflows/python/badge.svg\n\n## Description\n\nAt the same time as we developed [OneModel](https://github.com/sb2cl/onemodel), we created SBML2dae: a SBML-compatible python package which provides programming tools to generate SBML exporters to other programming languages for simulation or analysis.\nSBML2dae is open-source and complies with OneModel\'s design philosophy.\n\nBy default, SBML2dae only allows exporting SBML to Matlab.\nHowever, it is straightforward for an expert user to create a new parser for another programming language such as Modelica, Julia, or Python. \nWe expect more syntactic parsers to be incorporated using SBML2dae (by our group or by the community).\n\nThe differences with other Matlab parsers are (i) SBML2dae allows the simulation of algebraic loops (an indispensable element for the simulation of reduced-order models, using the quasi-steady-state approximation), (ii) it generates Matlab code using classes that significantly facilitates the integration of the models with the rest of Matlab tools and (iii) SBML2dae is easily modifiable to change the way of exporting the models.\n\n## Motivation\n\nThere are excellent tools for simulation and analysis of SBML models, but one of the most significant drawbacks is when the tool does not fit the needs of pre-existing workflows.\nSBML2dae solves this problem by allowing the user to implement customized SBML parsers that fit their particular workflow quickly.\n\n## How to setup\n\nSBML2dae can be installed from PyPI and is compatible with Python 3.7+ for Window, Mac and Linux.\n\nThe latest package can be installed with:\n\n```sh\npip install sbml2dae\n```\n\n## Quick example\n\nSBML2dae provides a simple command-line interface to export SBML models into Matlab code.\n\nGo to the examples folder in this repository and use the following command:\n```\nsbml2dae export ex01_simple_gene_expression.xml\n```\n\nIt will generate a `build` folder with the SBML model exported into Matlab.\n\n## Citing\n\nIf you use SBML2dae in your research, please use the following citations in your published works:\n\n- Santos-Navarro, F. N., Navarro, J. L., Boada, Y., Vignoni, A., & Picó, J. (2022). "OneModel: an open-source SBML modeling tool focused on accessibility, simplicity, and modularity." *DYCOPS*.\n\n- Santos-Navarro, F. N., Vignoni, A., & Picó, J. (2022). "Multi-scale host-aware modeling for analysis and tuning of synthetic gene circuits for bioproduction." *PhD thesis*.\n\n## License\n\nCopyright 2022 Fernando N. Santos-Navarro, Jose Luis Herrero, Yadira Boada, Alejandro Vignoni, and Jesús Picó\n\nLicensed under the Apache License, Version 2.0 (the "License"); you may not use this software except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.\n',
    'author': 'Fernando N. Santos Navarro',
    'author_email': 'fersann1@upv.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sb2cl/sbml2dae',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
