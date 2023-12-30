# {{ cookiecutter.package_name }}

{{ cookiecutter.short_description }}

{%- if cookiecutter.git_host == "GitLab" %}

[TOC]
{%- endif %}

## About the CI

The CI of this package is created to be as minimally invasive as possible.
Jobs, and thus the pipeline, only fail if they really cannot recover.
But this leads to a situation in which critical information is often not noticed, as the pipeline succeeds, even if there are problems with your code.
Thus, there are some job logs you should check by yourself from time to time.
Please see the following table with information what each job does and how it affects you.

{% if cookiecutter.git_host == "GitHub" -%}
| Job name | Short description | How it affects you/what you need to do |
| -------- | ----------------- | -------------------------------------- |
| `pytest` | Runs all tests defined in the `tests` folder and evaluate the coverage. | Will notify you of increases or decrease of the coverage on a per merge request basis. Also updates the coverage badge (if set up). |
| `flake8` | Looks for common mistakes in the style of the code. | On a regular basis, look through its output and determine if the recommendations are actionable. |
| `pylint` | Analyzes the code for errors or bad practices. | On a regular basis, look through its output and determine if the recommendations are actionable. |
| `mypy` | Runs a static type checker. | On a regular basis, look through its output and determine if the recommendations are actionable. |
| `publish` | Builds the package into a whl file and publishes it to <https://pypi.org/>. | The built package gets pushed to <https://pypi.org/>, from where you can install it via `pip install`. Requires a PyPI API token, see [New Release](#New-Release). |
| `release` | Releases the bundled code in GitHub. | You can link to the release for others to easily download a specific version (equivalent to tag) of your code. Runs on new tags of the format `v*.*.*`. |
{% elif cookiecutter.git_host == "GitLab" -%}
| Job name | Stage | Short description | How it affects you/what you need to do |
| -------- | ----- | ----------------- | -------------------------------------- |
{%- if cookiecutter.use_pre_commit == "yes" %}
| `pre-commit` | `.pre` | Runs the pre-commit pipeline. | Will fail if the pre-commit pipeline fails, can be modified to push resulting changes to autofix most problems.  |
{%- endif %}
| `install_deps` | `install_deps` | Installs and caches the package dependencies to speed up CI. | CI builds will be faster, as the dependencies are all already cached for later stages and future jobs.  |
| `code_quality` | `test` | Runs the code quality job from the template. | Will notify you of increases or decrease of the code quality on a per merge request basis.  |
| `pytest` | `test` | Runs all tests defined in the `tests` folder and evaluate the coverage. | Will notify you of increases or decrease of the coverage on a per merge request basis. Also updates the coverage badge (if set up). |
| `flake8` | `test` | Looks for common mistakes in the style of the code. | On a regular basis, look through its output and determine if the recommendations are actionable. |
| `pylint` | `test` | Analyzes the code for errors or bad practices. | On a regular basis, look through its output and determine if the recommendations are actionable. |
| `mypy` | `test` | Runs a static type checker. | On a regular basis, look through its output and determine if the recommendations are actionable. |
| `test-docs` | `test` | Test builds the documentation. | Builds the documentation to ensure it can be build successfully (runs only on non-default branches). |
| `publish` | `deploy` | Builds the package into a whl file and deploys it to the projects registry. | The built package gets pushed to the project's package registry, from where you can install it via `pip install`. Take a look the project's package registry for more details. |
| `pages` | `deploy` | Builds the documentation. | The built documentation will be available as a GitLab page of this project. |
| `prepare_job` | `prepare` | Runs preparation tasks for the `release_job` job. | No interaction required. |
| `release_job` | `release` | Releases the bundled code in GitLab. | You can link to the release for others to easily download a specific version (equivalent to tag) of your code. |
{% endif %}
## What to change

After installing the project via cookiecutter, you have to make minor changes to ensure a correct configuration.
Once you finished the changes, feel free to delete this section.
Most changes can be found via the TODO tag (`# TODO @{{ cookiecutter.author_email }}:`) and should be rather self-explanatory.
Nevertheless, following is some further information.

{% if cookiecutter.git_host == "GitHub" -%}
### CI/CD: [`.github/workflows/`](./.github/workflows/)

The GitHub CI is prepared to run most jobs at least against your specified Python version.
Nevertheless, sometimes it's useful to test against multiple versions at once, for example if your target systems can vary.
Here, the configuration enables you to specify multiple Python versions at once.
Inside the corresponding files, there is a matrix to define the Python version.
Per default yours looks something like

```yaml
jobs:
  <jobname>:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["{{ cookiecutter.python_version }}", ...]
```

However, you can define any number of Python versions, as long as they correspond to valid tags [at Pythons Docker Hub images](https://hub.docker.com/_/python/tags).
For example, if you want to run a specific job against Python 3.8, 3.9, and 3.10, the new strategy matrix should look something like this:

```yaml
jobs:
  <jobname>:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10"]
```
{%- elif cookiecutter.git_host == "GitLab" %}
### CI/CD: [`.gitlab-ci.yml`](./.gitlab-ci.yml)

The GitLab CI is prepared to run most jobs at least against your specified Python version.
Nevertheless, sometimes it's useful to test against multiple versions at once, for example if your target systems can vary.
Here, the configuration enables you to specify multiple Python versions at once.
Inside the `cache_builder`-job, there is a matrix to define the Python version.
Per default yours looks something like

```yaml
.python_settings_template: &python_settings
  ...
  parallel:
    matrix:
    - PYTHON_VERSION: ["{{ cookiecutter.python_version }}", ...]
```

However, you can define any number of Python versions, as long as they correspond to valid tags [at Pythons Docker Hub images](https://hub.docker.com/_/python/tags).
For example, if you want to run `pytest`, `flake8`, `pylint`, and `mypy` against Python 3.8, 3.9, and 3.10, the new parallel matrix should look something like this:

```yaml
.python_settings_template: &python_settings
  ...
  parallel:
    matrix:
    - PYTHON_VERSION: ["3.8", "3.9", "3.10"]
```
{%- endif %}

### [`setup.cfg`](./setup.cfg)

In the [`setup.cfg`](./setup.cfg), there are some places, you have to manually update.
This is mostly the project url in the GitLab.
We don't know the url a priori and thus cannot prepare it.

Also make sure to add your `install_requires`, e.g. `numpy`, `scipy`, `matplotlib`, etc.
Afterwards, the section should look something like this:

```toml
install_requires =
    matplotlib
    numpy
    scipy
```

## New Release

{% if cookiecutter.git_host == "GitHub" -%}
If you want to create a new release of your software, simply update the [`VERSION`](./VERSION) file with the new version number and push a tag with the same name.
Remember to use the `v*.*.*` format for the tag name.

GitHub will also automatically publish the newest release to PyPI, but it requires a PyPI API token.
To generate one, go to <https://pypi.org/manage/account/token/>, log in, and create a new token.
Afterwards, save the token in the GitHub repository secrets under the name `PYPI_API_TOKEN`.
{% elif cookiecutter.git_host == "GitLab" -%}
If you want to create a new release of your software, simply update the [`VERSION`](./VERSION) file with the new version number.
GitLab will take care of the rest using the CI pipeline.
Note, that a first release, based on the specified version, will be automatically created.

## Badges

GitLab has the ability to display badges via the project settings independent of the `README.md`.
They can help to display important information, such as the CI status, the latest release, and many more.
Here is a list of interesting badges, one might like to add to the project.
To add them to your project, go to `Settings` -> `General` (in the left burger menu) -> `Badges`.

| Name | Link | Badge image URL | Note |
| ---- | ---- | --------------- | ---- |
| pipeline status | <https://gitlab.com/%{project_path}/-/commits/%{default_branch}> | <https://gitlab.com/%{project_path}/badges/%{default_branch}/pipeline.svg> | Auto-generated by GitLab |
| coverage | <https://gitlab.com/%{project_path}/-/commits/%{default_branch}> | <https://gitlab.com/%{project_path}/badges/%{default_branch}/coverage.svg> | Requires tests in the `tests` folder and the `pytest` job |
| pylint | <https://gitlab.com/%{project_path}/-/jobs/artifacts/%{default_branch}/raw/public/lint/{{ cookiecutter.python_version }}/pylint.log?job=pylint> | <https://gitlab.com/%{project_path}/-/jobs/artifacts/%{default_branch}/raw/public/badges/{{ cookiecutter.python_version }}/pylint.svg?job=pylint: [{{ cookiecutter.python_version }}]> | Requires the `pylint` job |
| release | <https://gitlab.com/%{project_path}/-/releases> | <https://gitlab.com/%{project_path}/-/badges/release.svg> | Requires the `publish`, `prepare_job`, `release_job` jobs, links to the most recent release |

### Note regarding the `pylint` badges

As you can run your code against multiple versions of Python, see [What to change -> CI/CD](#CI/CD:-.gitlab-ci.yml), you'll be able to choose from multiple versions of the badge.
Or, you can display all versions, that's up to you.
Simply change the "{{ cookiecutter.python_version }}" in the link and badge image url to your desired version for the corresponding badge.
{%- endif %}

## Description

TODO @{{ cookiecutter.author_email }}: Describe the package in more detail.

## Installation

Install the package via

```shell
python3 -m pip install -e .
```

for basic features.
Or, if you also want to locally run tests, you can use

```shell
python3 -m pip install -e '.[tests]'
```

If you want to have _all_ the dependencies installed, use

```shell
python3 -m pip install -e '.[all]'
```

{%- if cookiecutter.use_pre_commit %}
This step is required if you are using pre-commit hooks.
Finally, to install the pre-commit hooks, run

```shell
pre-commit install
```

Now, prior to any commit, the hooks defined in [`.pre-commit-config.yaml`](./.pre-commit-config.yaml) will be ran.
A failure in any hook will block the commit.
Although, most of the errors, like formatting, will correct themselves.
You just have to re-add all changed files and commit again.

Alternatively, you can run the pipeline at any time to invoke changes before they block commits with

```shell
pre-commit run --all-files
```
{%- endif %}

## Usage

TODO @{{ cookiecutter.author_email }}: Indicate the intended use of the package.
