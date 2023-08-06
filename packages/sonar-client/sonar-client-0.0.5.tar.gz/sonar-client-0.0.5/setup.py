from importlib.metadata import entry_points

import setuptools


def get_file_content(filename: str) -> str:
    """Read content of a file as a string"""
    with open(filename, encoding="utf-8", mode="r") as file:
        return file.read()


setuptools.setup(
    name="sonar-client",
    description="Client library and CLI for sonarqube API",
    version="0.0.5",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["sonar-cli=sonar_client.__main__:cli"]},
    long_description=get_file_content("README.md"),
    long_description_content_type="text/markdown",
)
