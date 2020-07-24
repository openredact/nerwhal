from distutils.core import setup

from setuptools import find_packages

setup(
    name="nerwhal",
    version="0.1.0a",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    license="MIT",
    description="Find personally identifiable information in German texts using NER and rule based matching.",
    long_description=open("README.md").read(),
    install_requires=["spacy==2.3.2", "spacy-stanza==0.2.3", "stanza==1.0.1", "flashtext==2.7"],
)
