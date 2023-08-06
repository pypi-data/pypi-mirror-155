# secrets-mgmt-cli
A simple CLI for managing secrets in AWS Secrets Manager

[![PyPI](https://img.shields.io/pypi/v/secrets-mgmt-cli.svg)](https://pypi.org/project/secrets-mgmt-cli/)
[![Changelog](https://img.shields.io/github/v/release/william-cass-wright/secrets-mgmt-cli?include_prereleases&label=changelog)](https://github.com/william-cass-wright/secrets-mgmt-cli/releases)
[![Tests](https://github.com/william-cass-wright/secrets-mgmt-cli/workflows/Test/badge.svg)](https://github.com/william-cass-wright/secrets-mgmt-cli/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/william-cass-wright/secrets-mgmt-cli/blob/master/LICENSE)

A simple CLI for managing secrets in AWS Secrets Manager

## Installation

Install this tool using `pip`:

    pip install secrets-mgmt-cli

## Usage

For help, run:

    secrets-mgmt-cli --help

You can also use:

    python -m secrets_mgmt_cli --help

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd secrets-mgmt-cli
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest

## TODO
- add `_version.py` file with `__version__` dunder; how to handle this in setup.py?
- create project config file from secret (`~/.config/project_name/config`) using `ConfigHandler`
- write new secret from config file
- overwrite/upversion a secret (designate latest?) --> "archive" secrets by renaming them
