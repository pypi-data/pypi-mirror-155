# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snapsheets']

package_data = \
{'': ['*']}

install_requires = \
['Deprecated>=1.2.12,<2.0.0',
 'PyYAML>=6.0,<7.0',
 'docopt>=0.6.2,<0.7.0',
 'icecream>=2.1.2,<3.0.0',
 'loguru>=0.6.0,<0.7.0',
 'pendulum>=2.1.2,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'tomli>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['snapsheets = snapsheets.core:cli',
                     'snapsheets-next = snapsheets.next:cli']}

setup_kwargs = {
    'name': 'snapsheets',
    'version': '0.6.2',
    'description': 'Getting tired of downloading Google Spreadsheets one by one from the browser ?',
    'long_description': '![GitLab pipeline](https://img.shields.io/gitlab/pipeline/qumanote/snapsheets?style=for-the-badge)\n![PyPI - Licence](https://img.shields.io/pypi/l/snapsheets?style=for-the-badge)\n![PyPI](https://img.shields.io/pypi/v/snapsheets?style=for-the-badge)\n![PyPI - Status](https://img.shields.io/pypi/status/snapsheets?style=for-the-badge)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/snapsheets?style=for-the-badge)\n\n\n# Snapsheets\n\nGetting tired of downloading Google Spreadsheets one by one from the browser ?\n\nThis package enables to wget Google Spreadsheets without login.\n(Spreadsheets should be shared with public link)\n\n\n---\n\n# Where to get it\n\n```bash\n$ pip3 install snapsheets\n```\n\n# Usage\n\n```bash\n$ snapsheets -h\nusage: snapsheets [-h] [--config CONFIG] [--url URL] [--debug] [--version]\n\noptions:\n  -h, --help       show this help message and exit\n  --config CONFIG  set config directory (default: ./config/)\n  --url URL        copy and paste an URL of the Google spreadsheet\n  --debug          show more messages\n  --version        show program\'s version number and exit\n```\n\n- Use ``--url`` option to download single spreadsheet.\n- Use ``--config`` option to download multiple spreadsheets.\n  - create a directory for config files.\n  - create a config file in TOML format.\n\n\n## Documents\n\n- https://qumanote.gitlab.io/snapsheets/\n\n\n\n\n\n# Examples\n## with ``--url`` option\n\n```bash\n$ snapsheets --url="https://docs.google.com/spreadsheets/d/1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM/edit#gid=0"\n2022-06-09T08:09:30 | WARNING  | Directory varlogs not found. Switch to current directory.\n2022-06-09T08:09:31 | SUCCESS  | 🤖 Downloaded snapd/snapsheet.xlsx\n2022-06-09T08:09:31 | SUCCESS  | 🚀 Renamed to snapd/20220609T080931_snapsheet.xlsx\n```\n\n- Downloaded file is temporarily named as ``snapsheet.xlsx``, then renamed with current-time based prefix.\n\n\n\n\n## with ``--config`` option\n\n```bash\n$ snapsheets --config="config/"\n2022-06-09T08:05:47 | WARNING  | Directory varlogs not found. Switch to current directory.\n2022-06-09T08:05:48 | SUCCESS  | 🤖 Downloaded snapd/snapsheet.xlsx\n2022-06-09T08:05:48 | SUCCESS  | 🚀 Renamed to snapd/2022_toml_sample1.xlsx\n2022-06-09T08:05:49 | SUCCESS  | 🤖 Downloaded snapd/snapsheet.xlsx\n2022-06-09T08:05:49 | SUCCESS  | 🚀 Renamed to snapd/20220609_toml_sample3.csv\n```\n\n\n- Make ``./config/`` directory and place your TOML files.\n  - If ``./config/`` does not exist, it will search from ``. (current directory)``.\n- Downloaded files are saved to ``./snapd/`` directory\n  - If ``./snapd/`` does not exit, it will be saved in ``. (current directory)``.\n\n\n## with module ``import``\n\n```python\n>>> from snapsheets import Sheet\n>>> url = "https://docs.google.com/spreadsheets/d/1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM/edit#gid=0"\n>>> sheet = Sheet(url=url, desc="Get Sample Sheet")\n>>> sheet.snapshot()\n📣 Get Sample Sheet\n🤖 Downloaded snapd/snapsheet.xlsx\n🚀 Renamed to snapd/20220602T225044_snapsheet.xlsx\n```\n\n---\n# Other requirements\n\n- Install ``wget`` if your system doesn\'t have them\n- Make your spreadsheet available with shared link (OK with read-only)\n\n\n# PyPI package\n\n- https://pypi.org/project/snapsheets/\n\n![PyPI - Downloads](https://img.shields.io/pypi/dd/snapsheets?style=for-the-badge)\n![PyPI - Downloads](https://img.shields.io/pypi/dw/snapsheets?style=for-the-badge)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/snapsheets?style=for-the-badge)',
    'author': 'shotakaha',
    'author_email': 'shotakaha+py@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://qumanote.gitlab.io/snapsheets/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
