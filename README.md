# UpgradePipPackages

## Description

This package is a tool to upgrade python packages faster and easiest.

## Requirements
This package require:
 - python3
 - python3 Standard Library

## Installation
```bash
pip install UpgradePipPackages
```

## Usages

### Command line

```bash
pipupgrade -h                                # Help message
pipupgrade --help                            # Help message

pipupgrade                                   # Upgrade all packages

pipupgrade WebScripts UpgradePipPackages     # Upgrade WebScripts and UpgradePipPackages only

pipupgrade                                   # Upgrade all packages, using command line
python3 -m UpgradePipPackages                # Upgrade all packages, using python package
python3 UpgradePipPackages.pyz               # Upgrade all packages, using python executable
```

### Python script

```python
from UpgradePipPackages import main
main()
```

```python
import UpgradePipPackages
UpgradePipPackages.main()
```

## Links
 - [Pypi](https://pypi.org/project/UpgradePipPackages)
 - [Github](https://github.com/mauricelambert/UpgradePipPackages)
 - [Documentation](https://mauricelambert.github.io/info/python/code/UpgradePipPackages.html)
 - [Python executable](https://mauricelambert.github.io/info/python/code/UpgradePipPackages.pyz)

## License
Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).