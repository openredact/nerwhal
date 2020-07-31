# Nerwhal

_**:warning: Disclaimer :warning::**_ This is a prototype. Do not use for anything critical.

A Python module that finds personally identifiable information in unstructured texts using NER and rule based matching.

---

![Tests](https://github.com/openredact/nerwhal/workflows/Tests/badge.svg?branch=master)
![Black & Flake8](https://github.com/openredact/nerwhal/workflows/Black%20&%20Flake8/badge.svg?branch=master)
[![MIT license](https://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)

## Description

Nerwhal is a framework that helps find named entities in text. Recognizers uncover
mentions that can be used to identify persons, such as name, phone number or place of birth.

Note, that while the package is language agnostic, the included models and recognizers are for the **German** language.

_**:warning: Disclaimer :warning::**_ This is a prototype, which must not be used in production without further protections. For
the following reasons not all named entities can be found:
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
- and of course the good ol' regular expressions

The engines can be found in the [Backends Package](nerwhal/backends). The recognizers operate on these backends
and are located in the [Recognizers Package](nerwhal/example_recognizers).

## Usage

```python
from nerwhal import recognize, Config

config = Config("de", ["nerwhal/example_recognizers/email_recognizer.py"])

recognize("Ich heiße Luke und meine E-Mail ist luke@skywalker.com.", config=config)
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
pytest --cov-report term --cov=nerwhal
```

To skip tests that require the download of stanza models run:
```
pytest -m "not slow"
```

## License

[MIT License](https://github.com/openredact/nerwhal/blob/master/LICENSE)
