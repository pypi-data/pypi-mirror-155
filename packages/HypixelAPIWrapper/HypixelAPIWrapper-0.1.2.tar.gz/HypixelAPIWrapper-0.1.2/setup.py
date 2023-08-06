from setuptools import setup, find_packages

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="HypixelAPIWrapper",
    version="0.1.2",
    description="Small library to work with Hypixel public API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://HypixelAPIWrapper.readthedocs.io/",
    author="Houwy",
    author_email="nazandre1233@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["HypixelAPIWrapper"],
    include_package_data=True,
    install_requires=["requests", "python_nbt"]
)