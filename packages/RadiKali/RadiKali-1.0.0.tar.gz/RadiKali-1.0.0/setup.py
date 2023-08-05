
from ast import keyword
from setuptools import setup, find_packages

setup(
        name="RadiKali",
        version="1.0.0",
        packages=find_packages('src'),
        package_dir= {'': 'src'},
        author="someone",
        keyword="dangerous",
        description= "does nothing"
)