from setuptools import setup
from setuptools import find_packages

version = '0.0.6'

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name = 'pyacptrak',
    version = version,
    author = 'HeytalePazguato (Jorge Centeno)',
    author_email = 'Heytale.Pazguato@gmail.com',
    maintainer = 'HeytalePazguato',
    description = 'Create ACOPOStrak resources for projects, training, meetings, mappView widgets, etc...',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/HeytalePazguato/pyacptrak',
    project_urls = {
        'Bug Tracker': 'https://github.com/HeytalePazguato/pyacptrak/issues'
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    package_dir = {'': 'src'},
    packages = find_packages(where='src'),
    python_requires = '>=3.9',
    install_requires = [
        'svgwrite >= 1.4.0',
        'xmltodict >= 0.12.0',
        'numpy >= 1.22.3',
        'typeguard >= 2.13.3',
        'IPython >= 7.23.1',
        'typing >= 3.7'
    ],
    extras_require = {
        'dev': [
            'pytest >= 7.1'
        ],
    },
    include_package_data = True,
)