from setuptools import setup

setup(name='scenario',
      version='0.2.0',
      packages=['scenario'],
      install_requires=['pexpect'],
      entry_points={
          'console_scripts': [
              'scenario = scenario.__main__:main'
          ]
      },
      )