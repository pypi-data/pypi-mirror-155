![GitLab pipeline](https://img.shields.io/gitlab/pipeline/qumanote/snapsheets?style=for-the-badge)
![PyPI - Licence](https://img.shields.io/pypi/l/snapsheets?style=for-the-badge)
![PyPI](https://img.shields.io/pypi/v/snapsheets?style=for-the-badge)
![PyPI - Status](https://img.shields.io/pypi/status/snapsheets?style=for-the-badge)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/snapsheets?style=for-the-badge)


# Snapsheets

Getting tired of downloading Google Spreadsheets one by one from the browser ?

This package enables to wget Google Spreadsheets without login.
(Spreadsheets should be shared with public link)


---

# Where to get it

```bash
$ pip3 install snapsheets
```

# Usage

```bash
$ snapsheets -h
usage: snapsheets [-h] [--config CONFIG] [--url URL] [--debug] [--version]

options:
  -h, --help       show this help message and exit
  --config CONFIG  set config directory (default: ./config/)
  --url URL        copy and paste an URL of the Google spreadsheet
  --debug          show more messages
  --version        show program's version number and exit
```

- Use ``--url`` option to download single spreadsheet.
- Use ``--config`` option to download multiple spreadsheets.
  - create a directory for config files.
  - create a config file in TOML format.


## Documents

- https://qumanote.gitlab.io/snapsheets/





# Examples
## with ``--url`` option

```bash
$ snapsheets --url="https://docs.google.com/spreadsheets/d/1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM/edit#gid=0"
2022-06-09T08:09:30 | WARNING  | Directory varlogs not found. Switch to current directory.
2022-06-09T08:09:31 | SUCCESS  | 🤖 Downloaded snapd/snapsheet.xlsx
2022-06-09T08:09:31 | SUCCESS  | 🚀 Renamed to snapd/20220609T080931_snapsheet.xlsx
```

- Downloaded file is temporarily named as ``snapsheet.xlsx``, then renamed with current-time based prefix.




## with ``--config`` option

```bash
$ snapsheets --config="config/"
2022-06-09T08:05:47 | WARNING  | Directory varlogs not found. Switch to current directory.
2022-06-09T08:05:48 | SUCCESS  | 🤖 Downloaded snapd/snapsheet.xlsx
2022-06-09T08:05:48 | SUCCESS  | 🚀 Renamed to snapd/2022_toml_sample1.xlsx
2022-06-09T08:05:49 | SUCCESS  | 🤖 Downloaded snapd/snapsheet.xlsx
2022-06-09T08:05:49 | SUCCESS  | 🚀 Renamed to snapd/20220609_toml_sample3.csv
```


- Make ``./config/`` directory and place your TOML files.
  - If ``./config/`` does not exist, it will search from ``. (current directory)``.
- Downloaded files are saved to ``./snapd/`` directory
  - If ``./snapd/`` does not exit, it will be saved in ``. (current directory)``.


## with module ``import``

```python
>>> from snapsheets import Sheet
>>> url = "https://docs.google.com/spreadsheets/d/1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM/edit#gid=0"
>>> sheet = Sheet(url=url, desc="Get Sample Sheet")
>>> sheet.snapshot()
📣 Get Sample Sheet
🤖 Downloaded snapd/snapsheet.xlsx
🚀 Renamed to snapd/20220602T225044_snapsheet.xlsx
```

---
# Other requirements

- Install ``wget`` if your system doesn't have them
- Make your spreadsheet available with shared link (OK with read-only)


# PyPI package

- https://pypi.org/project/snapsheets/

![PyPI - Downloads](https://img.shields.io/pypi/dd/snapsheets?style=for-the-badge)
![PyPI - Downloads](https://img.shields.io/pypi/dw/snapsheets?style=for-the-badge)
![PyPI - Downloads](https://img.shields.io/pypi/dm/snapsheets?style=for-the-badge)