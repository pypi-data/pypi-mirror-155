# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geowrangler']

package_data = \
{'': ['*']}

install_requires = \
['fastcore>=1.4,<2.0',
 'geopandas>=0.10,<0.11',
 'numpy>=1.21,<2.0',
 'pandas>=1.2,<2.0']

setup_kwargs = {
    'name': 'geowrangler',
    'version': '0.1.0.dev1',
    'description': 'Tools for dealing with geospatial data',
    'long_description': "# Geowrangler\n> Tools for wrangling with geospatial data\n\n## Overview\n\n**Geowrangler** is a python package for geodata wrangling. It helps you build data transformation workflows with no out-of-the-box solutions from other geospatial libraries.\n\nWe have surveyed our past geospatial projects to extract these solutions for our work and hope it will be useful for others as well.\n\nOur audience are researchers, analysts and engineers delivering geospatial projects.\n\nWe [welcome your comments, suggestions, bug reports and code contributions](https://github.com/thinkingmachines/geowrangler/issues) to make **Geowrangler** better. \n\n### Modules\n\n* Grid Tile Generation\n* Geometry Validation \n* Vector Zonal Stats \n* Raster Zonal Stats (_planned_)\n* Geometry Simplification (_planned_)\n* Grid Tile Spatial Imputation (_planned_)\n\n## Installation\n\n```\npip install git+https://github.com/thinkingmachines/geowrangler.git\n```\n\n## Documentation\n\nThe documentation for [the package is available here](https://geowrangler.web.app)\n\n## Development\n\n### Development Setup\n\nIf you want to learn more about **Geowrangler** and explore its inner workings,\nyou can setup a local development environment. You can run geowrangler's jupyter notebooks\nto see how the different modules are built and how they work. \n\nPlease ensure you are using python `3.7` or higher\n\n```\npip install pre-commit poetry\npre-commit install\npoetry install\npoetry run pip install pip --upgrade\npoetry run pip install -e .\n```\n### Jupyter Notebook Development\n\nThe code for the **geowrangler** python package resides in Jupyter notebooks located in the `notebooks` folder.\n\nUsing [nbdev](https://nbdev.fast.ai), we generate the python modules residing in the `geowrangler` folder from code cells in jupyter notebooks marked with an `#export` comment. A `#default_exp <module_name>` comment at the first code cell of each notebook directs `nbdev` to put the code in a module named `<module_name>` in the `geowrangler` folder. \n\nSee the [nbdev cli](https://nbdev.fast.ai/cli.html) documentation for more details on the commands to generate the package as well as the documentation.\n### Running notebooks\n\nRun the following to view the jupyter notebooks in the `notebooks` folder\n\n```\npoetry run jupyter lab\n```\n### Generating and viewing the documentation site\n\nTo generate and view the documentation site on your local machine, the quickest way is to setup [Docker](https://docs.docker.com/get-started/). The following assumes that you have setup docker on your system.\n```\npoetry run nbdev_build_docs --mk_readme False --force_all True\ndocker-compose up jekyll\n```\n\nAs an alternative if you don't want to use _Docker_ you can [install jekyll](https://jekyllrb.com/docs/installation/) to view the documentation site locally.\n\n`nbdev` converts notebooks within the `notebooks/` folder into a jekyll site.\n\nFrom this jekyll site, you can then create a static site.\n\nTo generate the docs, run the following\n\n```\n\npoetry run nbdev_build_docs -mk_readme False --force_all True\ncd docs && bundle i && cd ..\n\n```\n\nTo run the jekyll site, run the following\n\n```\ncd docs\nbundle exec jekyll serve\n```\n\n### Running tests\n\nWe are using `pytest` as our test framework. To run all tests and generate a generate a coverage report, run the following.\n\n```\npoetry run pytest --cov --cov-config=.coveragerc -n auto\n```\n\n\nTo run a single test or test file\n\n```shell\n# for a single test function\npoetry run pytest tests/test_grids.py::test_create_grids\n# for a single test file\npoetry run pytest tests/test_grids.py\n```\n### Contributing\n\nPlease read [CONTRIBUTING.md](https://github.com/thinkingmachines/geowrangler/blob/master/CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](https://github.com/thinkingmachines/geowrangler/blob/master/CODE_OF_CONDUCT.md) before anything.\n\n",
    'author': 'Thinking Machines',
    'author_email': 'geowrangler@thinkingmachin.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thinkingmachines/geowrangler',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
