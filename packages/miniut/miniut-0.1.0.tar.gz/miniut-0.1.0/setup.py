from setuptools import find_packages, setup
from os import path
import re


# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

def get_version(prop):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open( 'src/miniut/__init__.py').read())
    return result.group(1)

setup(
    name='miniut',
    version = get_version('__version__'),
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    description='Paquete de utilidades',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Juan Sebastián Martínez Serna',
    url='https://github.com/JuanS3/utilities',
    project_urls={
        'Bug Tracker' : 'https://github.com/JuanS3/utilities/issues',
        'Wiki' : 'https://github.com/JuanS3/utilities/wiki'
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8"
)
