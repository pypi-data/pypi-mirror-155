#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['batchspawner', 'jupyter-rsession-proxy', 'datasize', 'humanize', 'boto3',
                'aws-pcluster-helpers']

test_requirements = []

setup(
    author=" Jillian Rowe",
    author_email='jillian@dabbleofdevops.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Extend Jupyterhub's BatchSpawner to deal with AWS ParallelCluster's SLURM environment",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='aws_pcluster_slurm_spawner',
    name='aws_pcluster_slurm_spawner',
    packages=find_packages(include=['aws_pcluster_slurm_spawner', 'aws_pcluster_slurm_spawner.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/dabble-of-devops-bioanalyze/aws_pcluster_slurm_spawner',
    version='0.3.0',
    zip_safe=False,
)
