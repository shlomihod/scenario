from setuptools import setup

setup(name='scenario',
      version='0.4.0',
      packages=['scenario', 'scenario.player'],
      install_requires=['pexpect'],
      entry_points={
          'console_scripts': [
              'scenario = scenario.__main__:main'
          ]
      },
      test_suite='nose.collector',
	  tests_require=['nose'],
      )
