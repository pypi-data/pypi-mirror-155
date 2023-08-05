from os import path

from setuptools import setup
from setuptools import find_packages

DIR = path.dirname(path.abspath(__file__))

with open(path.join(DIR, 'README.md')) as f:
    README = f.read()

with open(path.join(DIR, 'requirements.txt')) as f:
    INSTALL_PACKAGES = f.read().splitlines()

setup(
    name='mw-feature-serving-sdk',
    version='0.1.1',
    packages=find_packages(exclude=("tests",)),
    url='https://www.mobilewalla.com',
    license='',
    author='Mobilewalla Feature Store',
    author_email='feature-store@mobilewalla.com',
    description='An SDK to access Mobilewalla\'s Feature Machine service',
    long_description=README,
    long_description_content_type='text/markdown',
    python_requires='>=3.7',
    install_requires=INSTALL_PACKAGES
)
