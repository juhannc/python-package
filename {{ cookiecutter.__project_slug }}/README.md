<!--
SPDX-FileCopyrightText: {{ cookiecutter.__year }} {{ cookiecutter.author_name }}

SPDX-License-Identifier: {{ cookiecutter.license }}
-->
# {{ cookiecutter.package_name }}

{{ cookiecutter.short_description }}

{%- if cookiecutter.git_host == "GitLab" %}

[TOC]
{%- endif %}

## Description

TODO @{{ cookiecutter.author_email }}: Describe the package in more detail.

## Installation

### Install uv

See the [uv documentation](https://docs.astral.sh/uv/getting-started/installation/).

On Linux/macOS run

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

and on Windows run

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Create virtualenv

Simply run

```shell
uv venv
```

### Install autosafe

```shell
uv sync
```

## Development

### Add a new python dependency

```shell
uv add <package>
```

or, in a not-uv environment:

```shell
uv add --active <package>
```

## Usage

TODO @{{ cookiecutter.author_email }}: Indicate the intended use of the package.
