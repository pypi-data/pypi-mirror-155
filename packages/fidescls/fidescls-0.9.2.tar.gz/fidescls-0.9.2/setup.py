import pathlib
from setuptools import setup, find_packages

import versioneer

here = pathlib.Path(__file__).parent.resolve()
long_description = open("docs/fidescls/docs/installation/pypi.md").read()

# Requirements
install_requires = open("requirements.txt").read().strip().split("\n")
dev_requires = open("dev-requirements.txt").read().strip().split("\n")

setup(
    name="fidescls",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="CLI for Fidescls",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ethyca/fidescls",
    entry_points={"console_scripts": ["fidescls=fidescls.cli.context:cli"]},
    python_requires=">=3.8, <4",
    package_dir={"fidescls": "fidescls"},
    packages=find_packages(),
    author="Ethyca, Inc.",
    author_email="fidesteam@ethyca.com",
    license="Apache License 2.0",
    install_requires=install_requires,
    dev_requires=dev_requires,
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
    ],
)
