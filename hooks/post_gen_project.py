import gzip
import os
import re
import shutil
import urllib.request

import reuse.download

REMOVE_PATHS = [
    "{% if cookiecutter.git_host != 'GitHub' %} .github {% endif %}",
    "{% if cookiecutter.git_host != 'GitLab' %} .gitlab-ci.yml {% endif %}",
]


FIX_CI_FILES = [
    ".github/workflows/flake8.yml",
    ".github/workflows/mypy.yml",
    ".github/workflows/pylint.yml",
    ".github/workflows/pytest.yml",
    ".gitlab-ci.yml",
]


def get_highest_python_major_minor() -> str:
    url = "https://www.python.org/doc/versions/"
    with urllib.request.urlopen(url) as response:
        data = response.read()
    # handle possible gzip-compressed response
    if isinstance(data, bytes):
        try:
            if data[:2] == b"\x1f\x8b":
                html = gzip.decompress(data).decode("utf-8", errors="replace")
            else:
                html = data.decode("utf-8", errors="replace")
        except Exception:
            html = data.decode("latin-1", errors="replace")
    else:
        html = str(data)
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


def main() -> None:
    for path in REMOVE_PATHS:
        path = path.strip()
        if path and os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.unlink(path)

    versions_list = generate_list_of_python_versions(
        min_ver="{{ cookiecutter.python_version }}",
        max_ver=get_highest_python_major_minor(),
    )
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

    spdx = "{{ cookiecutter.license }}"
    reuse.download.put_license_in_file(spdx, f"LICENSES/{spdx}.txt")


if __name__ == "__main__":
    main()
