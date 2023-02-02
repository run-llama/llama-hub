"""Set up the package."""
import sys
from pathlib import Path

from setuptools import find_packages, setup

name = "loader_hub"

with open(Path(__file__).absolute().parents[0] / name / "VERSION") as _f:
    __version__ = _f.read().strip()

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

install_requires = [
    "dataclasses_json",
]

setup(
    name=name,
    version=__version__,
    packages=find_packages(),
    description="Library of data loaders for LLMs.",
    install_requires=install_requires,
    long_description=long_description,
    license="MIT",
    url="https://github.com/emptycrown/loader-hub",
    include_package_data=True,
    long_description_content_type="text/markdown",
)
