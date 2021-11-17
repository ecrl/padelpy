import os
from setuptools import setup


def get_readme():
    """Load README.rst for display on PyPI."""
    with open('README.md') as fhandle:
        return fhandle.read()


VERSION = get_version_info()

setup(
    name='padelpy',
    version=VERSION,
    description='A Python wrapper for PaDEL-Descriptor',
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/ecrl/padelpy',
    author='Travis Kessler',
    author_email='Travis_Kessler@student.uml.edu',
    license='MIT',
    packages=['padelpy'],
    install_requires=[],
    package_data={
        'padelpy': [
            'PaDEL-Descriptor/*',
            'PaDEL-Descriptor/lib/*',
            'PaDEL-Descriptor/license/*'
        ]
    },
    zip_safe=False
)
