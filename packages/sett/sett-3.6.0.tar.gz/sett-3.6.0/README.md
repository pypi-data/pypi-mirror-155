[![pipeline status](https://gitlab.com/biomedit/sett/badges/master/pipeline.svg)](https://gitlab.com/biomedit/sett/-/commits/master)
[![coverage report](https://gitlab.com/biomedit/sett/badges/master/coverage.svg)](https://gitlab.com/biomedit/sett/-/commits/master)
[![documentation status](https://readthedocs.org/projects/sett/badge/)](https://sett.readthedocs.io/)
[![license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![python version](https://img.shields.io/pypi/pyversions/sett.svg?logo=python&logoColor=white)](https://pypi.org/project/sett)
[![latest version](https://img.shields.io/pypi/v/sett.svg)](https://pypi.org/project/sett)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# SETT - Secure Encryption and Transfer Tool

_sett_ enables packaging, encryption, and transfer of data to preconfigured locations.

## Documentation

Detailed documentation as well as a quick-start guide can be found in the
[sett documentation](https://sett.readthedocs.io).

For the latest, non-stable, version of the docs, see [here](<https://sett.readthedocs.io/en/latest/>).

### Documentation quick-links

* [Requirements and installation](https://sett.readthedocs.io/en/stable/installation.html).
* [Quick-start guide](https://sett.readthedocs.io/en/stable/quick_start.html).
* [Creating and managing GnuPG keys with sett](https://sett.readthedocs.io/en/stable/key_management.html).
* [Using sett to encrypt, transfer and decrypt data](https://sett.readthedocs.io/en/stable/usage.html)

## Unit tests coverage

Please note that a number of gui-specific files are excluded from the unit
tests coverage. The detailed list of excluded files can be found in
[`pyproject.toml`](pyproject.toml), under the `[tool.coverage.run]` section.
