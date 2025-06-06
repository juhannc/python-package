import re
import sys

VERSION_REGEX = r"^(\d+\.)?(\d+\.)?(\*|\d+)$"

version = "{{ cookiecutter.version }}"

if not re.match(VERSION_REGEX, version):
    print(f"ERROR: {version} is not a valid version!")
    sys.exit(1)
