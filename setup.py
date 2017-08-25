import sys
from setuptools import setup

if sys.version_info[0] != 2:
    sys.stderr.write('This package only supports Python 2.\n')
    sys.exit(1)

setup(name='scenario',
      version='2.1.0',
      packages=['scenario',
                'scenario.player',
                'scenario.parser',
                'scenario.tests'],
      package_dir={'scenario': 'scenario'},
      package_data={'scenario': ['formats/html/index.html',
                                 'formats/html/*/*',
                                 'schema/*']},
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2 :: Only',
      ],
      install_requires=['pexpect', 'jsonschema'],
      entry_points={
          'console_scripts': [
              'scenario = scenario.__main__:main'
          ]
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      )
