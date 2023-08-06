# SBML2dae: a customizable SBML to Matlab parser

[![GitHub Actions][github-actions-badge]](https://github.com/sb2cl/sbml2dae/actions)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[github-actions-badge]: https://github.com/sb2cl/sbml2dae/workflows/python/badge.svg

## Description

At the same time as we developed [OneModel](https://github.com/sb2cl/onemodel), we created SBML2dae: a SBML-compatible python package which provides programming tools to generate SBML exporters to other programming languages for simulation or analysis.
SBML2dae is open-source and complies with OneModel's design philosophy.

By default, SBML2dae only allows exporting SBML to Matlab.
However, it is straightforward for an expert user to create a new parser for another programming language such as Modelica, Julia, or Python. 
We expect more syntactic parsers to be incorporated using SBML2dae (by our group or by the community).

The differences with other Matlab parsers are (i) SBML2dae allows the simulation of algebraic loops (an indispensable element for the simulation of reduced-order models, using the quasi-steady-state approximation), (ii) it generates Matlab code using classes that significantly facilitates the integration of the models with the rest of Matlab tools and (iii) SBML2dae is easily modifiable to change the way of exporting the models.

## Motivation

There are excellent tools for simulation and analysis of SBML models, but one of the most significant drawbacks is when the tool does not fit the needs of pre-existing workflows.
SBML2dae solves this problem by allowing the user to implement customized SBML parsers that fit their particular workflow quickly.

## How to setup

SBML2dae can be installed from PyPI and is compatible with Python 3.7+ for Window, Mac and Linux.

The latest package can be installed with:

```sh
pip install sbml2dae
```

## Quick example

SBML2dae provides a simple command-line interface to export SBML models into Matlab code.

Go to the examples folder in this repository and use the following command:
```
sbml2dae export ex01_simple_gene_expression.xml
```

It will generate a `build` folder with the SBML model exported into Matlab.

## Citing

If you use SBML2dae in your research, please use the following citations in your published works:

- Santos-Navarro, F. N., Navarro, J. L., Boada, Y., Vignoni, A., & Picó, J. (2022). "OneModel: an open-source SBML modeling tool focused on accessibility, simplicity, and modularity." *DYCOPS*.

- Santos-Navarro, F. N., Vignoni, A., & Picó, J. (2022). "Multi-scale host-aware modeling for analysis and tuning of synthetic gene circuits for bioproduction." *PhD thesis*.

## License

Copyright 2022 Fernando N. Santos-Navarro, Jose Luis Herrero, Yadira Boada, Alejandro Vignoni, and Jesús Picó

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this software except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
