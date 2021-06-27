import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

VERSION = '0.2.2'
DESCRIPTION = 'Libary for repeated execution of functions at specific times.'

setup(
    name="reptaskorg",
    version=VERSION,
    author="Cedric Klimt",
    author_email="cekl@gmx.net",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[],
    license='MIT',
    url="https://github.com/CeKl/reptaskorg",
    py_modules=["reptaskorg"],

    keywords=['python', 'execute functions repeatedly'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
)
