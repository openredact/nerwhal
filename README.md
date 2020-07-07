# PII Identifier

_**:warning: Disclaimer :warning::**_ This is a prototype. Do not use for anything critical.

A Python module that finds personally identifiable information in unstructured texts using NER and rule based matching.

---

![Tests](https://github.com/openredact/pii-identifier/workflows/Tests/badge.svg?branch=master)
![Black & Flake8](https://github.com/openredact/pii-identifier/workflows/Black%20&%20Flake8/badge.svg?branch=master)
[![MIT license](https://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)

## Description

PII Identifier is a framework that helps find PIIs (Personally Identifiable Information) in text. Recognizers uncover
mentions that can be used to identify persons, such as name, phone number or place of birth.

Note, that while the package is language agnostic, the included models and recognizers are for the **German** language.

_**:warning: Disclaimer :warning::**_ This is a prototype, which must not be used in production without further protections. For
the following reasons not all PIIs can be found:
- the set of recognizers is not exhaustive
- the rules of each recognizer do not cover all of the ways in which information can be expressed; the limitations of
each recognizer are to the best of our knowledge noted in its code documentation.
- the statistical models used are not perfect and cannot be expected uncover all occurrences of the named entities that
they are looking for
- further this is a work in process which may contain bugs
Further note, that the recognizers may return false positive finds. This work is limited to identifying named
entities in the given text and that many indirect indicators as well as linkage with other data is out-of-scope.


## Features

The recognizers are built on top of powerful NLP engines:
- [spaCy](https://github.com/explosion/spaCy) for statistical NER and rule based matching on a token level
- [flair](https://github.com/flairNLP/flair) for statistical NER
- and of course the good ol' regular expressions

The engines can be found in the [Backends Package](pii_identifier/backends). The recognizers operate on these backends
and are located in the [Recognizers Package](pii_identifier/recognizers).

## Usage

```
from pii_identifier import find_piis

piis = find_piis(your_text)
```

## Development

### Install requirements

You can install all requirements using:

```
pip install -r requirements.txt
```

Compared to installation with `setup.py`, [requirements.txt](requirements.txt) additionally installs developer dependencies.

To install it using `setup.py` run:

```
pip install .
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
pytest --cov-report term --cov=pii_identifier
```

To skip slow tests run:
```
pytest --doctest-modules -m "not slow"
```

## License

MIT