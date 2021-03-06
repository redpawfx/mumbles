#
# THIS FILE IS PART OF THE MUMBLES PROJECT AND IS LICENSED UNDER THE GPL.
# SEE THE 'COPYING' FILE FOR DETAILS
#
# libnotify Mumbles Plugin 
#
#------------------------------------------------------------------------

from setuptools import setup
import sys, os
from shutil import copy

__author__ = 'dot_j <dot_j@mumbles-project.org>'
__doc__ = 'A simple plugin for mumbles that listens for libnotify messages'
__version__ = '0.1'

setup(
	name='LibNotifyMumbles',
	version=__version__,
	description=__doc__,
	author=__author__,
	packages=['libnotifymumbles'],
	package_dir={'libnotifymumbles':'src'},
	entry_points='''
	[mumbles.plugins]
	LibNotifyMumbles = libnotifymumbles:LibNotifyMumbles
	'''
)

# copy egg file to plugin directory
copy("dist/LibNotifyMumbles-%s-py%d.%d.egg" %(__version__,sys.version_info[0],sys.version_info[1]), "../../")

