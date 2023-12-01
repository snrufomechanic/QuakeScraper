from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='QuakeScraper',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'branca',
        'certifi',
        'charset-normalizer',
        'folium',
        'idna',
        'Jinja2',
        'MarkupSafe',
        'numpy',
        'pandas',
        'python-dateutil',
        'pytz',
        'requests',
        'six',
        'urllib3',
        'tzdata'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)