# nexio-behave

The Nexio Behave

Features:

- <!-- list of features -->

Table of Contents:

- [Installation](#installation)
- [Guide](#guide)
- [Development](#development)

## Installation

nexio-behave requires Python 3.9 or above.

```bash
pip install nexio-behave
# or
poetry add nexio-behave
```

## Guide

<!-- Subsections explaining how to use the package -->

## Development

To develop nexio-behave, install dependencies and enable the pre-commit hook:

```bash
pip install pre-commit poetry
poetry install
pre-commit install -t pre-commit -t pre-push
```

To run tests:

```bash
poetry run pytest
```
