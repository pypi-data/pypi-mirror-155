# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['koda_ac']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.2,<4.0.0', 'rich>=12.4.4,<13.0.0', 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['koda = koda_ac.__main__:cli']}

setup_kwargs = {
    'name': 'koda-ac',
    'version': '0.1.4',
    'description': '',
    'long_description': '# About\n\nThis is a project for the Data Compression course at Warsaw University of Technology.\n\n# Installation & Usage\n\nPython >= 3.9 & pip is required\n\nWe recommend using pipx [pipx](https://pypa.github.io/pipx/) to install the program as an executable isolated inside a dedicated Python virtual environment:\n\n```\n> python3 -m pip install pipx\n> python3 -m pipx ensurepath\n> pipx install koda_ac\n> koda --help\nUsage: koda [OPTIONS] COMMAND [ARGS]...\n```\n\nAlternatively, a standard `pip install` should work:\n\n```\n> python3 -m pip install koda_ac\n> python3 -m koda_ac --help\nUsage: python -m koda_ac [OPTIONS] COMMAND [ARGS]...\n```\n\n# Development setup\n\n[Poetry](https://python-poetry.org) is used for dependency management, see https://python-poetry.org/docs/master/#installation for installation instructions.\n\nAfter installing Poetry, use `poetry install` to install project dependencies.\n\n## Makefile tasks\n\n- use `make format` to format code with `black` and `isort`\n- use `make lint` to lint code with `mypy` and `flake8`\n- use `make test` to run tests in `tests/` with `pytest`',
    'author': 'Michał Rokita',
    'author_email': 'mrokita@mrokita.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mRokita/KODA',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
