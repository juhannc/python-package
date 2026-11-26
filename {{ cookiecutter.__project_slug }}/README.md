<!--
SPDX-FileCopyrightText: {{ cookiecutter.__year }} {{ cookiecutter.author_name }}

SPDX-License-Identifier: {{ cookiecutter.license }}
-->
# {{ cookiecutter.package_name }}

[![The latest version of {{ cookiecutter.package_name }} can be found on PyPI.](https://img.shields.io/pypi/v/{{ cookiecutter.package_name }}.svg)](https://pypi.python.org/pypi/{{ cookiecutter.package_name }})
[![Information on what versions of Python {{ cookiecutter.package_name }} supports can be found on PyPI.](https://img.shields.io/pypi/pyversions/{{ cookiecutter.package_name }}.svg)](https://pypi.python.org/pypi/{{ cookiecutter.package_name }})
[![Python tests (pytest)](https://github.com/{{ cookiecutter.author_name }}/{{ cookiecutter.package_name }}/actions/workflows/pytest.yaml/badge.svg)](https://github.com/{{ cookiecutter.author_name }}/{{ cookiecutter.package_name }}/actions/workflows/pytest.yaml)
[![Coverage](https://codecov.io/gh/{{ cookiecutter.author_name }}/{{ cookiecutter.package_name }}/graph/badge.svg)](https://codecov.io/gh/{{ cookiecutter.author_name }}/{{ cookiecutter.package_name }})
[![Docs status](https://readthedocs.org/projects/{{ cookiecutter.package_name }}/badge/)](https://{{ cookiecutter.package_name }}.readthedocs.io/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
[![prek](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json)](https://github.com/{{ cookiecutter.author_name }}/{{ cookiecutter.package_name }})
[![REUSE status](https://api.reuse.software/badge/github.com/{{ cookiecutter.author_name }}/{{ cookiecutter.package_name }})](https://api.reuse.software/info/github.com/{{ cookiecutter.author_name }}/{{ cookiecutter.package_name }})
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)

{{ cookiecutter.short_description }}

{%- if cookiecutter.git_host == "GitLab" %}

[TOC]
{%- endif %}

## Description

TODO @{{ cookiecutter.author_email }}: Describe the package in more detail.

## Installation

We recommend using [uv](https://astral.sh/uv/) to manage the virtual environment and dependencies.
Simply running `uv sync` will create a virtual environment and install all dependencies as specified in `pyproject.toml`.

## Usage

TODO @{{ cookiecutter.author_email }}: Indicate the intended use of the package.

### CLI

{{ cookiecutter.package_name }} provides a command-line interface (CLI) for easy interaction.
After installing the package, you can use the `{{ cookiecutter.package_name }}` command in your terminal:

```shell
uv run {{ cookiecutter.package_name }} --help
```

This will list all available commands and options.
They are described in detail in the [documentation](https://{{ cookiecutter.package_name }}.readthedocs.io/).

### Common CLI Commands

Here are the most frequently used commands:

### API

TODO @{{ cookiecutter.author_email }}: Indicate the intended API use here. Python code blocks will be picked up and evaluated automatically by pytest.

## License

Copyright and license information are provided in accordance to the [REUSE Specification 3.3](https://reuse.software/spec-3.3/).
