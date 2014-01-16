#
# THIS FILE IS PART OF THE MUMBLES PROJECT AND IS LICENSED UNDER THE GPL.
# SEE THE 'COPYING' FILE FOR DETAILS
#
# Rythmbox Mumbles Plugin
#
#------------------------------------------------------------------------

from setuptools import setup
import sys, os
from shutil import copy

__author__ = 'dot_j <dot_j@mumbles-project.org>'
__doc__ = 'A simple rhythmbox input plugin for mumbles'
__version__ = '0.1'

setup(
	name='RhythmboxMumblesInput',
	version=__version__,
	description=__doc__,
	author=__author__,
	packages=['rhythmbox'],
	package_dir={'rhythmbox':'src'},
	package_data={'':['themes/rhythmbox.xpm']},
	entry_points='''
	[mumbles.plugins]
	RhythmboxMumblesInput = rhythmbox:RhythmboxMumblesInput
	'''
)

# copy egg file to plugin directory
copy("dist/RhythmboxMumblesInput-%s-py%d.%d.egg" %(__version__,sys.version_info[0],sys.version_info[1]), "../../")
