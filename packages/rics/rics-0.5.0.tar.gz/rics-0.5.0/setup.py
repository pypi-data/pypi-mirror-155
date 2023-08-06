# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rics',
 'rics._internal_support',
 'rics.cardinality',
 'rics.mapping',
 'rics.translation',
 'rics.translation.dio',
 'rics.translation.fetching',
 'rics.translation.offline',
 'rics.utility',
 'rics.utility.perf']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.1', 'pyyaml>=5.3', 'sqlalchemy>=1.1.0']

setup_kwargs = {
    'name': 'rics',
    'version': '0.5.0',
    'description': 'My personal little ML engineering library.',
    'long_description': '# Readme\n\n<div align="center">\n\n[![PyPI - Version](https://img.shields.io/pypi/v/rics.svg)](https://pypi.python.org/pypi/rics)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rics.svg)](https://pypi.python.org/pypi/rics)\n[![Tests](https://github.com/rsundqvist/rics/workflows/tests/badge.svg)](https://github.com/rsundqvist/rics/actions?workflow=tests)\n[![Codecov](https://codecov.io/gh/rsundqvist/rics/branch/main/graph/badge.svg)](https://codecov.io/gh/rsundqvist/rics)\n[![Read the Docs](https://readthedocs.org/projects/rics/badge/)](https://rics.readthedocs.io/)\n[![PyPI - License](https://img.shields.io/pypi/l/rics.svg)](https://pypi.python.org/pypi/rics)\n\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\n\n</div>\n\n\nMy personal little ML engineering library.\n\n* GitHub repo: <https://github.com/rsundqvist/rics.git>\n* Documentation: <https://rics.readthedocs.io>\n* Free software: MIT\n\n## Features\n\n* Multivariate performance testing - [with plots!](https://rics.readthedocs.io/en/latest/utility-perftest.html)\n* An extensible [ID translation suite](https://rics.readthedocs.io/en/latest/translation-quickstart.html), including SQL integration for retrival of data\n* Various other utilities methods - \n  from [logging configuration](https://rics.readthedocs.io/en/latest/utility-logging.html)\n  to [fetching data from the web](https://rics.readthedocs.io/en/latest/utility-data-download.html)\n* Two-directional mapping implementation in `rics.mapping`\n\n## Quickstart for development\n\n### Notice\nThis project uses groups for extras dependencies, which is currently a **PRERELEASE** feature (slated for `1.2`). Assuming\npoetry was installed the recommended way (see below), this can be done using:\n```bash\ncurl -sSL https://install.python-poetry.org/ | python -\npoetry self update --preview 1.2.0a2\n```\n\n### Setting up for local development\nAssumes a "modern" version of Ubuntu (guide written under `Ubuntu 20.04.2 LTS`) with basic dev dependencies installed.\n\nThis project uses groups for extras dependencies. If installation fails, make sure that output from `poetry --version` \nis `1.2.0` or greater.\n\nTo get started, run the following commands:\n\n1. Installing the latest version of Poetry\n   ```bash\n   curl -sSL https://install.python-poetry.org/ | python -\n   ```\n\n2. Installing the project\n   ```bash\n   git clone git@github.com:rsundqvist/rics.git\n   cd rics\n   poetry install --with dev-extras\n   inv install-hooks\n   ./run-invocations\n   ```\n   The last step is optional, but serves to verify that the project is ready-to-run.\n\n### Registering the project on Codecov\n\nProbably only for forking?\n```bash\ncurl -Os https://uploader.codecov.io/latest/linux/codecov\nchmod +x codecov\n```\n\nVisit https://app.codecov.io and log in, follow instructions to link the repo and get a token for private repos.\n```bash\nCODECOV_TOKEN="<from-the-website>"\ninv coverage --fmt=xml\n./codecov -t ${CODECOV_TOKEN}\n```\n\n## Credits\n\nThis package was created with [Cookiecutter][cookiecutter] and\nthe [fedejaure/cookiecutter-modern-pypackage][cookiecutter-modern-pypackage] project template.\n\n[cookiecutter]: https://github.com/cookiecutter/cookiecutter\n\n[cookiecutter-modern-pypackage]: https://github.com/fedejaure/cookiecutter-modern-pypackage\n',
    'author': 'Richard Sundqvist',
    'author_email': 'richard.sundqvist@live.se',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rsundqvist/rics',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
