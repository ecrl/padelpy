from setuptools import setup

setup(
    name='padelpy',
    version='0.1.10',
    description='A Python wrapper for PaDEL-Descriptor',
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
