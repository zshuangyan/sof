from setuptools import setup

setup(name='sof',
      packages=['sof'],
      entry_points = {
          'console_scripts': ['sof=sof.sof:command_line_runner']
      }
)
