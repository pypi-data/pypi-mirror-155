# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_storages']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.78.0']

setup_kwargs = {
    'name': 'fastapi-storages',
    'version': '0.0.0',
    'description': 'Fastapi Storages',
    'long_description': "# Fastapi Storages\n\nCollection of backend storages and orm extensions to simplify file management in fastapi projects. This project\nis inspired by the [django-storages](https://github.com/jschneier/django-storages) packages. If you have  suggestion for a storage backend that is not \nyet supported, please [open an issue](https://github.com/Tobi-De/fastapi-storages/issues/new) and will discuss it.\n\n[![PyPI](https://img.shields.io/pypi/v/fastapi-storages.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/fastapi-storages.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/fastapi-storages)][python version]\n[![License](https://img.shields.io/pypi/l/fastapi-storages)][license]\n\n[![Read the documentation at https://fastapi-storages.readthedocs.io/](https://img.shields.io/readthedocs/fastapi-storages/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/Tobi-De/fastapi-storages/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/Tobi-De/fastapi-storages/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/fastapi-storages/\n[status]: https://pypi.org/project/fastapi-storages/\n[python version]: https://pypi.org/project/fastapi-storages\n[read the docs]: https://fastapi-storages.readthedocs.io/\n[tests]: https://github.com/Tobi-De/fastapi-storages/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/Tobi-De/fastapi-storages\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n\n## Features\n\n### Media storage backend\n\n- [ ] Local\n- [ ] Amazon ses\n- [ ] Google cloud\n- [ ] Deta\n\n### Database extensions\n\n- [ ] Tortoise ORM\n- [ ] RedisOM\n- [ ] Beanie\n- [ ] SQLModel\n\n## Installation\n\nYou can install _Fastapi Storages_ via [pip] from [PyPI]:\n\n```console\n$ pip install fastapi-storages\n```\n\n## Quickstart\n\n```python\n\n```\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Fastapi Storages_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/Tobi-De/fastapi-storages/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/Tobi-De/fastapi-storages/blob/main/LICENSE\n[contributor guide]: https://github.com/Tobi-De/fastapi-storages/blob/main/CONTRIBUTING.md\n[command-line reference]: https://fastapi-storages.readthedocs.io/en/latest/usage.html\n",
    'author': 'Tobi DEGNON',
    'author_email': 'tobidegnon@proton.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Tobi-De/fastapi-storages',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
