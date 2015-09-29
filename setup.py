
'''
    The proper way to install this package is use pip to install it. If you
    want to install this local copy, use this command:

        pip install .

    If you don't use pip to install, then 'pip uninstall' won't work as
    expected.
'''

from distutils.core import setup
from setuptools import find_packages
from os import listdir
from os.path import dirname, join, isfile, isdir
import sys

import gocd_parser.version

setup_dir = dirname(__file__)
package_name = 'uh_build_monitor'

scripts = []
for thing in listdir('bin'):
    path = join('bin', thing)
    if isfile(path):
        scripts.append(path)

install_requires=open(join(setup_dir, 'requirements.txt')).readlines()

setup(
    name=package_name,
    version='0.3',
    description='Raspberry PI & Unicorn HAT build monitor',
    author='Jon Barber & Iain Miller',
    author_email='jon.barber@acm.org',
    url='https://github.com/sneakybeaky/pi-build-monitor',
    package_dir={ package_name: 'uh_build_monitor' },
    packages=find_packages(),
    install_requires=install_requires,
    scripts=scripts
)