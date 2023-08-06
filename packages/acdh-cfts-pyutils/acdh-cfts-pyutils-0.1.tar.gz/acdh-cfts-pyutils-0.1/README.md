[![Test](https://github.com/acdh-oeaw/acdh-cfts-pyutils/actions/workflows/test.yml/badge.svg)](https://github.com/acdh-oeaw/acdh-cfts-pyutils/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/acdh-oeaw/acdh-cfts-pyutils/branch/master/graph/badge.svg?token=JF7T9ID1MM)](https://codecov.io/gh/acdh-oeaw/acdh-cfts-pyutils)
[![flake8 Lint](https://github.com/acdh-oeaw/acdh-cfts-pyutils/actions/workflows/lint.yml/badge.svg)](https://github.com/acdh-oeaw/acdh-cfts-pyutils/actions/workflows/lint.yml)


# acdh-cfts-pyutils
Python Package to interact with a dedicated Typesense Server and Collection

* This package exposes some constants to interact with a dedicated Typesense Server and Collection through other Python scripts. 
* Also this package is inteded to be the one and only place to modifiy the schema of the given centralised collection

## install

* run `pip install acdh-cfts-pyutils`
* adapt/modifiy environmet variables to fit you needs. See `env.default` for example. If you use this package to populate the ACDH-CH central fulltext search collection running on ACDH-CH's own Typesense-Server, you'll only need to set `TYPESENSE_API_KEY` via an environment varibale.
