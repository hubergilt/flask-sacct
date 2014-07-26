#!/usr/bin/env python
from setuptools import setup
import os

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

VERSION = [l for l in open('flask_sacct/__init__.py').readlines()
                if l.startswith('__version__ = ')][0].split("'")[1]

setup(
    name='flask-sacct',
    version='0.1',
    url='https://www.github.com/jcollas/flask-sacct/',
    author = 'Julien Collas',
    author_email = 'jul.collas@gmail.com',
    description='Slurm Workload Manager accounting webservice',
    long_description = README,
    packages = ['flask_sacct'],
    include_package_data = True,
    platforms='any',
    install_requires=[
        'Flask',
    ],
    entry_points = {
        'console_scripts': [
            'flask-sacct = flask_sacct.core:run_server'
        ]
    },
)
