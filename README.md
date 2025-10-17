# Python Package Template

A simple but versatile template for python packages.

This cookiecutter template provides an easy way to create a new python package.
It supports a basic CI for both GitLab as well as GitHub and provides a basic setup for testing.

## uv (Recommended)

See the [uv documentation](https://docs.astral.sh/uv/getting-started/installation/).

On Linux/macOS run

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

and on Windows run

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Usage

To create a new python package, run the following command:

```shell
uvx --with jinja2-time cookiecutter gh:juhannc/python-package
```
