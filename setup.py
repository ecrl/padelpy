import os
from setuptools import setup


def get_readme():
    """Load README.rst for display on PyPI."""
    with open('README.md') as fhandle:
        return fhandle.read()


def get_version_info():
    """Read __version__ from version.py, using exec, not import."""
    fn_version = os.path.join("padelpy", "version.py")
    myglobals = {}
    with open(fn_version, "r") as f:
        # pylint: disable=exec-used
        exec(f.read(), myglobals)
    return myglobals["__version__"]


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
