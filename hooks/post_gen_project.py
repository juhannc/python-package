import os
import re
import shutil
import urllib.request

REMOVE_PATHS = [
    "{% if cookiecutter.use_pre_commit == false %} .pre-commit-config.yaml {% endif %}",
    "{% if cookiecutter.git_host != 'GitHub' %} .github {% endif %}",
    "{% if cookiecutter.git_host != 'GitLab' %} .gitlab-ci.yml {% endif %}",
    "{% if cookiecutter.git_host != 'GitLab' %} .codeclimate.yml {% endif %}",
]


FIX_CI_FILES = [
    ".github/workflows/flake8.yml",
    ".github/workflows/mypy.yml",
    ".github/workflows/pylint.yml",
    ".github/workflows/pytest.yml",
    ".gitlab-ci.yml",
    "README.md",
]


def get_highest_python_major_minor() -> str:
    url = "https://www.python.org/doc/versions/"
    with urllib.request.urlopen(url) as response:
        html = response.read()
    matches = re.search(r"Python 3\.[1-9]([0-9]*)\.[1-9]([0-9]*)", str(html))
    version = re.search(r"3\.[1-9]([0-9]*)", str(matches[0]))
    return version[0]


def generate_list_of_python_versions(min_ver: str, max_ver: str) -> str:
    min_minor = int(min_ver.split(".")[1])
    max_minor = int(max_ver.split(".")[1])
    versions = []
    for minor in range(min_minor, max_minor + 1):
        versions.append(f'"3.{minor}"')
    return ", ".join(versions)


for path in REMOVE_PATHS:
    path = path.strip()
    if path and os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)

try:
    versions_list = generate_list_of_python_versions(
        min_ver="{{ cookiecutter.python_version }}",
        max_ver=get_highest_python_major_minor(),
    )
except:
    versions_list = "{{ cookiecutter.python_version }}"

for file in FIX_CI_FILES:
    try:
        with open(file, "r") as f:
            data = f.read()
            data = data.replace(
                r'["{{ cookiecutter.python_version }}", ...]', f"[{versions_list}]"
            )
        with open(file, "w") as f:
            f.write(data)
    except:
        pass
