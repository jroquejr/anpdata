import os
from setuptools import setup, find_packages


with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name         = 'project',
    version      = '1.0',
    install_requires = required,
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = frentista.settings']},
)
