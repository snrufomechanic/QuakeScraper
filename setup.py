from setuptools import setup, find_packages

setup(
    name='QuakeScraper',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pandas',
    ],
)