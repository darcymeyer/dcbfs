from setuptools import setup

setup(name='dcbfs',
      version='0.1',
      description='Distributed Cloud Based File System',
      author='Darcy Meyer',
      author_email='dmeyer@andover.edu',
      url='darcymeyer.github.io',
      packages=['dcbfs'],
      entry_points = {
              'console_scripts': [
                  'dcbfs = dcbfs.shell:main',                  
              ],              
          },
     )
