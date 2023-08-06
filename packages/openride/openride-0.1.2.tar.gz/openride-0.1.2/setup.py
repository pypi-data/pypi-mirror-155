from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

requirements = [
    "shapely",
    "numba",
    "numpy",
    "dataclasses",
    "vtk>=9.1.0",
    "matplotlib",
    "multipledispatch",
]

setup(
    name="openride",
    version="0.1.2",
    author="Jean-Luc Déziel",
    author_email="jluc1011@hotmail.com",
    url="https://gitlab.com/jldez/openride",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
)
