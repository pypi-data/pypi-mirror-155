#!/usr/bin/env python
import pathlib
import setuptools 

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not
            line.startswith("#")]


setuptools.setup(
    name="m2-template_fill",
    version="0.0.1",
    author="March",
    author_email="m2.march@gmail.com",
    description="Tools for using Jinja as an application.",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=parse_requirements('requirements.txt'),
    scripts=['scripts/template_fill'],
    python_requires=">=3.6",
    license='MIT'
)
