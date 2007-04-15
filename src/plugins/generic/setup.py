#
# THIS FILE IS PART OF THE MUMBLES PROJECT AND IS LICENSED UNDER THE GPL.
# SEE THE 'COPYING' FILE FOR DETAILS
#
# Generic Mumbles Plugin
#
#------------------------------------------------------------------------

from setuptools import setup

__author__ = 'dot_j <dot_j@mumbles-project.org>'
__doc__ = 'A default plugin for mumbles'

setup(
	name='GenericMumbles',
	version='0.1',
	description=__doc__,
	author=__author__,
	packages=['generic'],
	entry_points='''
	[mumbles.plugins]
	GenericMumbles = generic:GenericMumbles
	'''
)

