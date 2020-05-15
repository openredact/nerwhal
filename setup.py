from distutils.core import setup

from setuptools import find_packages

setup(
    name="pii-identifier",
    version="0.1.0a",
    packages=find_packages(exclude=["tests"]),
    package_data={"pii_identifier": ["pii_identifier/recognizers/data/*.csv"]},
    include_package_data=True,
    license="MIT",
    description="Find personally identifiable information in German texts using NER and rule based matching.",
    long_description=open("README.md").read(),
    install_requires=[
        "spacy==2.2.4",
        # TODO this will not work for distribution on PyPI, see
        #  https://stackoverflow.com/questions/53383352/spacy-and-spacy-models-in-setup-py
        #  prefer a solution with download on first usage, ideally to a folder shared by all venvs (e.g. ~/.spacy
        "de_core_news_sm@"
        "https://github.com/explosion/spacy-models/releases/download/de_core_news_sm-2.2.5/de_core_news_sm-2.2.5.tar.gz",
        "flair==0.4.5",
    ],
)
