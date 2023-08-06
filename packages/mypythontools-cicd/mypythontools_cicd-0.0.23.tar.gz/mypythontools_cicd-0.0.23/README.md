# mypythontools

Module with functionality around Continuous Integration and Continuous Delivery.

[![Python versions](https://img.shields.io/pypi/pyversions/mypythontools_cicd.svg)](https://pypi.python.org/pypi/mypythontools_cicd/) [![PyPI version](https://badge.fury.io/py/mypythontools_cicd.svg)](https://badge.fury.io/py/mypythontools_cicd) [![Downloads](https://pepy.tech/badge/mypythontools_cicd)](https://pepy.tech/project/mypythontools_cicd) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Malachov/mypythontools_cicd.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Malachov/mypythontools_cicd/context:python) [![Documentation Status](https://readthedocs.org/projects/mypythontools_cicd/badge/?version=latest)](https://mypythontools_cicd.readthedocs.io/en/latest/?badge=latest) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![codecov](https://codecov.io/gh/Malachov/mypythontools_cicd/branch/master/graph/badge.svg)](https://codecov.io/gh/Malachov/mypythontools_cicd)

Why to use this and not Travis or Circle CI? It's local and it's fast. You can setup it as a task in IDE and
if some phase fails, you know it soon and before pushing to repo.

You can also import mypythontools in your CI/CD and use it there of course.

If you are not sure whether the structure of your app will work with this code, check `project-starter-cookiecutter` on [GitHub](https://github.com/Malachov/project-starter-cookiecutter).

## Links

Official documentation - [readthedocs](https://mypythontools.readthedocs.io/)

Official repo - [GitHub](https://github.com/Malachov/mypythontools)


## Installation

Python >=3.6 (Python 2 is not supported).

Install with

```console
pip install mypythontools
```

## Subpackages
Package is divided into several subpackages

### build
Build your application to .exe with pyinstaller. It also builds javascript frontend with npm build if configured, which is used mostly in PyVueEel applications.

### deploy
Build package and push it to PyPi.

### misc
Miscellaneous functions that are too small to have own subpackage.

### project_paths
Subpackage where you can get paths used in your project (path to README,  \_\_init__.py etc.).

### project_utils
In project utils you can find many functions for CI/CD like formatting, docs creation, version setting etc.
There is also pipelining function that will call them in defined order.

### tests
Runs tests in more venvs with different python versions, also with wsl linux if configured and create coverage.

## Mypythontools

There is extra library in separate repository which is not about CICD, but normal python helpers.

https://github.com/Malachov/mypythontools

This can help you with a lot of stuff around CICD like getting project paths, generating docs, testing,
deploying to PyPi etc.

**subpackages**

- config
- misc
- paths
- plots
- property
- terminal
- type_hints