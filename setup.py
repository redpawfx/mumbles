#!/usr/bin/env python

from distutils.core import setup
import os
import glob

dist = setup(name='mumbles',
	version='0.4',
	author='dot_j',
	author_email='dot_j@mumbles-project.org',
	maintainer='dot_j',
	maintainer_email='dot_j@mumbles-project.org',
	description='Mumbles is notification system for the Gnome desktop.',
	long_description='Mumbles is a plugin-driven, DBus based notification system written for the Gnome desktop. Similar to libnotify notifications and Growl for OSX (http://growl.info), Mumbles aims to provide a modern notification system for the GNU/Linux Desktop.',
	url='http://www.mumbles-project.org/',
	download_url='http://www.mumbles-project.org/download',
	license='GNU GPL',
	platforms='linux',
	scripts=['bin/mumbles', 'bin/mumbles-send'],
	packages=['mumbles'],
	package_dir={'mumbles': 'src'},
	data_files=[
		('share/icons/hicolor/22x22/apps', ['src/ui/mumbles.png']),
		('share/icons/hicolor/scalable/apps', ['src/ui/mumbles.svg']),
		('share/pixmaps', ['src/ui/mumbles.png']),
		('share/applications', ['bin/mumbles.desktop']),
		('bin', glob.glob("src/themes/mumbles-small/*.png"))
	],
	package_data={ 'mumbles' :
		["ui/*.glade",
		 "ui/mumbles.png",
		 "plugins/2.4_plugs/*.egg",
		 "plugins/2.5_plugs/*.egg",
		 "plugins/2.6_plugs/*.egg",
		 "plugins/2.7_plugs/*.egg",
		 "plugins/icons/*.png",
		 "themes/default/*.xml",
		 "themes/default/*.png",
		 "themes/blue/*.xml",
		 "themes/blue/*.png",
		 "themes/glass/*.xml",
		 "themes/glass/*.png",
		 "themes/human/*.xml",
		 "themes/human/*.png",
		 "themes/mumbles-round/*.xml",
		 "themes/mumbles-round/*.png",
		 "themes/mumbles-small/*.xml",
		 "themes/mumbles-small/*.png"
		]
	}
)
