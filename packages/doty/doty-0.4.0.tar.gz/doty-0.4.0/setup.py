#!/usr/bin/env python
#
# Copyright (C) 2022 Leah Lackner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import find_packages, setup


def read_file(file: str) -> str:
    with open(file, "r") as f:
        return f.read().strip()


def read_requirements(file: str) -> list[str]:
    return [
        line.strip()
        for line in read_file(file).split("\n")
        if not line.startswith("#") and line.strip()
    ]


setup_info = dict(
    name="doty",
    version="0.4.0",
    author="Leah Lackner",
    author_email="leah.lackner+github@gmail.com",
    url="https://github.com/leahevy/doty",
    project_urls={
        "Documentation": "https://github.com/leahevy/"
        "doty"
        "/blob/master/README.md",
        "Source": "https://github.com/leahevy/doty",
        "Tracker": "https://github.com/leahevy/" "doty/issues",
    },
    description="A Python project template.",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    platforms="Linux, Mac OSX",
    license="GPLv3",
    include_package_data=True,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General"
        " Public License v3 or later (GPLv3+)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.10",
    ],
    zip_safe=True,
    entry_points={
        "console_scripts": ["doty=doty.cli:main"],
    },
    package_dir={"": "."},
    packages=find_packages(where="."),
    python_requires=">=3.10",
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": read_requirements("requirements-dev.txt"),
    },
    cmdclass={},
)
setup(**setup_info)  # type: ignore
