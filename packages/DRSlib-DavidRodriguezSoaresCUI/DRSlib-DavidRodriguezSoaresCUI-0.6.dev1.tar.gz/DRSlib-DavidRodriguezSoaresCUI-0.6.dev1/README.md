# [DRSlib - a set of utilities by DavidRodriguezSoaresCUI](https://github.com/DavidRodriguezSoaresCUI/DRSlib)

DRSlib is a Python package that provides a wide range of small
yet powerful and highly-reusable functions, classes, 
decorators, etc. Its main purpose is to provide high-level
"building blocks" that accomplish simple tasks, facilitating
the writing of elaborate scripts with limited code.

License: see LICENSE file.

Author: DavidRodriguezSoaresCUI

## Install

You can install DRSlib using the pip package manager:
- On Unix/macOS: ```python3 -m pip install DRSlib-DavidRodriguezSoaresCUI```
- On Windows: ```python -m pip install DRSlib-DavidRodriguezSoaresCUI```

You may need to use elevated permissions to install a package, or use a variation of this command on your specific system. There are plenty of tutorials on the Internet if you need help.


## Documentation

You can find documentation in source code docstrings, or, more practically, by building
documentation from source:

- On `Windows`: Run `sphinx-full-rebuild.bat` from directory `docs`
- On `Linux`: If your shell is bash compatible, run `sphinx-full-rebuild.sh` from directory `docs`. If not, you should be capable of adapting it to your system.

*Building documentation* requires installing packages ``sphinx`` and ``furo`` you can install in one of these ways:
- ``pip install -r requirements-documentation.txt``
- ``pip install sphinx furo``

## Versioning

This package adheres to [PEP 440](https://www.python.org/dev/peps/pep-0440), specifically follows version scheme example `"major.minor" versioning with developmental releases, release candidates and post-releases for minor corrections`.

Note: `major.minor.dev*` releases are not intended for users, these are quick iterations for development. When author decides there was enough changes and `DRSlib` is ready for a new user release, a corresponding `major.minor` release will be made available.


## Packaging

I followed [this python.org tutorial](https://packaging.python.org/tutorials/packaging-projects/). See the [package page on Pypi](https://pypi.org/project/DRSlib-DavidRodriguezSoaresCUI/)


## Warning to users

**DRSlib** is a quickly evolving package, and author doesn't take any responsibility to maintain it or to keep
its API stable, but will make a good faith effort to do so. Also, some of its code writes to the disk, so its use 
may lead to data loss.

Use it at your own risk.
