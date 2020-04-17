# German PII Identifier

A Python module finds personally identifiable information in **German** texts using NER and rule based matching.

_**Disclaimer:**_ **This is a prototype only, which must not be used in production. The set of indicators is incomplete
and not sufficient for a reliable identification of all personally identifiable information. Furthermore, the code may
still contain bugs. The statistical models used will not be able to find all personally identifiable information
and may also return false positives. The same is true for all other detection methods employed. Note that indirect
indicators are not considered in this prototype.**

![Tests](https://github.com/langhabel/pii-identifier/workflows/Tests/badge.svg?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)


## Development

### Install dev requirements

```
pip install -r requirements-dev.txt
```

### Install the pre-commit hooks

```
pre-commit install
git config --bool flake8.strict true  # Makes the commit fail if flake8 reports an error
```

To run the hooks:
```
pre-commit run --all-files
```

### Testing

The tests can be executed with:
```
pytest --doctest-modules --cov-report term --cov=pii_identifier
```
To skip slow tests run:
```
pytest --doctest-modules -m "not slow"
```
