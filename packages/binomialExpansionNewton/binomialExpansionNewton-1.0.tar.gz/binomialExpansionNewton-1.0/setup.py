from setuptools import setup, Distribution, find_packages

setup(
    name='binomialExpansionNewton',
    version='1.0',
    description='Implementacja Dwumianu Newtona',
    packages=find_packages(),
    package_data={
        '': ['binomialExpansion.dll'],
    },
    distclass=Distribution
)
