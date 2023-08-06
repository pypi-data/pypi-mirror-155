from setuptools import setup, Distribution, find_packages

setup(
    name='binomialExpansionModule',
    version='2.0',
    description='Implementacja Dwumianu Newtona',
    packages=find_packages(),
    package_data={
        '': ['binomialExpansion.dll'],
    },
    distclass=Distribution
)
