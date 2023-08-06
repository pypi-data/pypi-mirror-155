#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ 
    'fire==0.4.0',
    'omegaconf==2.2.2',
    'ripgrepy==1.1.0'
]

test_requirements = ['pytest>=3', ]

setup(
    author="pysourcesfetcher",
    author_email='noreply@local.lab',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python3 module and cli tool to retrieve useful info from sources code in various languages.",
    entry_points={
        'console_scripts': [
            'pysourcesfetcher=pysourcesfetcher.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pysourcesfetcher',
    name='pysourcesfetcher',
    packages=find_packages(include=['pysourcesfetcher', 'pysourcesfetcher.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/weallfloatdownhere/pysourcesfetcher',
    version='0.1.0',
    zip_safe=False,
)
