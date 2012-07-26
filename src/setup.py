from setuptools import setup
import os

setup(
    name = 'safood',
    version = '0.1',
    url = 'https://github.com/dinosaurkfb/safood.git',
    license = 'BSD',
    author = 'dinosaurkfb',
    author_email = 'kfbuniversity@gmail.com',
    description = 'built for people who want safe food',
    zip_safe = False,
    platforms = 'any',
    package_dir = {'': 'common'},
    include_package_data = True,
)
