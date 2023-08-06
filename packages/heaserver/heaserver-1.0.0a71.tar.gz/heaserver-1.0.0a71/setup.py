"""
Documentation for setup.py files is at https://setuptools.readthedocs.io/en/latest/setuptools.html
"""

from setuptools import setup, find_namespace_packages


# Import the README.md file contents
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='heaserver',
      version='1.0.0a71',
      description='The server side of HEA.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://risr.hci.utah.edu',
      author='Research Informatics Shared Resource, Huntsman Cancer Institute, Salt Lake City, UT',
      author_email='Andrew.Post@hci.utah.edu',
      python_requires='>=3.10',
      package_dir={'': 'src'},
      packages=find_namespace_packages(where='src'),
      package_data={'heaserver.service': ['py.typed']},
      install_requires=[
          'heaobject~=1.0.0a30',
          'aiohttp[speedups]~=3.8.1',
          'aiohttp-remotes~=1.2.0',
          'motor~=2.5.1',
          'pytz~=2021.3', # We should get rid of this dependency and switch to the built-in zoneinfo module after we no longer need python 3.8 support.
          'tzlocal~=4.1',
          'uritemplate~=4.1.1',
          'accept-types~=0.4.1',
          'mongoquery~=1.3.6',
          'jsonschema~=4.4.0',
          'jsonmerge~=1.8.0',
          'requests>=2.27',
          'types-requests>=2.27',  # Should be set at same version as requests.
          'boto3==1.21.38',
          'botocore==1.24.38',
          'boto3-stubs[essential]==1.21.38',
          'botocore-stubs[essential]==1.24.38',
          'freezegun~=1.2.1',
          'regex~=2022.4.24'
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: Software Development',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Scientific/Engineering :: Medical Science Apps.'
      ]
      )
