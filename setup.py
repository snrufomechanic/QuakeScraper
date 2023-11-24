# setup.py

from setuptools import setup

setup(
    name='QuakeScraper',
    version='0.1',
    packages=['src'],
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pandas'
    ],
)
