# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['texbld',
 'texbld.cli',
 'texbld.clients',
 'texbld.common',
 'texbld.common.image',
 'texbld.common.project',
 'texbld.docker',
 'texbld.parser',
 'texbld.parser.v1',
 'texbld.scaffold']

package_data = \
{'': ['*'], 'texbld.scaffold': ['sample_image/*']}

install_requires = \
['docker>=5.0.3,<6.0.0',
 'jsonschema>=4.5.1,<5.0.0',
 'requests>=2.28.0,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'urllib3>=1.26.9,<2.0.0']

entry_points = \
{'console_scripts': ['texbld = texbld.cli:run']}

setup_kwargs = {
    'name': 'texbld',
    'version': '0.1.1',
    'description': 'A dockerized build tool for paper compilation',
    'long_description': '# texbld\n\nAlthough we expect LaTeX compilation to be a declarative process (source to\nPDF), the compilations for large projects eventually require a large number of\ncustom external programs and dependencies. For example, a compilation step might\nrequire running a script written in haskell, piping that output into pandoc,\nthen putting everything into a LaTeX file for compilation with `pdflatex`. Good\nluck installing all of those programs (ESPECIALLY the pesky ghc dependencies) in\na production system!\n\nFurthermore, different LaTeX distributions will have ever so slightly different\noutputs (especially when working with biblatex), which is an issue for\nreproducibility.\n\nThe first take on these problems was\n[mktex](https://github.com/junikimm717/mktex). Although it solves some\ndependency issues, it suffers from the various fragility and reproducibility\nissues that come with using pre-built docker images. Furthermore, because of its\ndesign, these images were forced to be monolithic, bloated, and ultimately\ninflexible. Each build should have exactly the dependencies that it requires\nand nothing more!\n\n`texbld` aims to solve these problems by providing an environment where build images\nare fully reproducible and shareable. It uses docker for absolute system\nreproducibility and for usage across all platforms which it supports (MacOS,\nWindows, and its native Linux).\n\nImage hashes are used to ensure that any docker image is **completely immutable**,\npreventing dependency modification issues.\n\nUsers can specify their build image in a simple TOML file (along with associated\nfiles) and upload them to github, from which it can be inherited and used by\nother people in their own projects. _Extensive Documentation will be released in the future._\n\nImages can be inherited from packages in the local filesystem, GitHub, or Docker.\n\n## Installation\n\nThe project is live on [pypi](https://pypi.org/project/texbld/).\nRun `pip install texbld`.\n\n## Setting Up This Project\n\nThis project uses poetry as its dependency manager. Simply run `poetry install`\nand `poetry shell` inside the project directory, and you should land in a\nvirtual environment with all of your dependencies.\n\nIn order to run tests in the virtual environment, run `pytest`.\n\n## The Local Environment\n\nThe project configuration file should be in `(project root)/texbld.toml`, while\nlocal image configurations should be in `$HOME/.config/texbld/packages`.\n',
    'author': 'junikimm717',
    'author_email': 'junikimm717@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/texbld/texbld',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
