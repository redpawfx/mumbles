#!/usr/bin/python
##################################################
# Check twitter for new messages
#   Copyright (c) 2008 dot_j <dot_j[AT]mumbles-project[DOT]org>
#   Lisenced under the GPL
##################################################
# twitter account information
USERNAME=''
PASSWORD=''

# how often (in milliseconds) to check for updates
UPDATE_INTERVAL=60000 # 10 minutes

# max number of notifications to show at a
# time (if more notification that this are
# received, NotifyNum signal is sent, just
# informing the number of new notifications
MAX_NOTIFICATIONS = 10

# show debug information
DEBUG = True
##################################################

import os,sys
sys.path.append("/Volumes/luma/_globalSoft/python/thirdParty/mumbles/mumblesSource-0.4/plugins/twittercheck")

import twitter
import gobject
import rfc822
from urllib2 import HTTPError
import dbus
import dbus.service
import dbus.glib
#from dbus.mainloop.glib import DBusGMainLoop
import getopt


TWITTER_DBUS_INTERFACE = 'com.twitter.DBus'
TWITTER_DBUS_PATH = '/com/twitter/DBus'

class Usage(Exception):
    def __init__(self, msg=None):
        app = sys.argv[0]
        if msg != 'help':
                self.msg = app+': Invalid options. Try --help for usage details.'
        else:
            self.msg = \
                        app+": DBus notifications on new Twitter messages.\n" \
                        "Copyright (C) 2008 dot_j <dot_j[AT]mumbles-project[DOT]org>\n" \
                        "Lisenced under the GPL\n\n" \
                        "Usage: mumbles [options]\n\n" \
                        "-h, --help\n" \
                        "\tPrint a summary of the command-line usage of "+app+".\n" \
                        "-p, --public\n" \
                        "\tCheck Public Timeline.\n" \

class TwitterCheck(dbus.service.Object):
    def __init__(self, public_only=False):
        self._public_only = public_only

        session_bus = dbus.SessionBus()
        bus_name = dbus.service.BusName(TWITTER_DBUS_INTERFACE, bus=session_bus)
        dbus.service.Object.__init__(self, bus_name, TWITTER_DBUS_PATH)

        self.api = twitter.Api(username=USERNAME, password=PASSWORD)
        self.interval = UPDATE_INTERVAL
        self.notifyLimit = MAX_NOTIFICATIONS
        self.debug = DEBUG

        self.lastCheck = None

        self.minInterval = 60000 # 1 minute min refresh interval
        if self.interval < self.minInterval:
            print "Warning: Cannot check twitter more often than once a minute! Using default of 1 minute."
            self.interval = self.minInterval
        self._check()

    @dbus.service.signal(dbus_interface=TWITTER_DBUS_INTERFACE, signature='isssss')
    def Notify(self, id, created, relative_create, name, screen_name, text):
        pass

    @dbus.service.signal(dbus_interface=TWITTER_DBUS_INTERFACE, signature='i')
    def NotifyNum(self, num):
        pass

    def unescape(self, s):
        s = s.replace("&lt;", "<")
        s = s.replace("&gt;", ">")
        s = s.replace("&apos;", "'")
        s = s.replace("&quot;", '"')
        # this has to be last:
        s = s.replace("&amp;", "&")
        return s

    def _check(self):
        if self.debug:
            if self.lastCheck:
                print "checking timeline (newer than %s):" %(self.lastCheck)
            else:
                print "checking timeline:"

        try:
            if USERNAME != '' and not self._public_only:
                print "  checking friends timeline"
                timeline = self.api.GetFriendsTimeline(since=self.lastCheck)
            else:
                if USERNAME == '':
                    print "  no user name set, checking public timeline"
                elif self._public_only:
                    print "  checking public timeline"
                timeline = self.api.GetPublicTimeline()
        except HTTPError, e:
            timeline = list()
            # if error other than not modified
            if e.code != 304:
                print "HTTPError: %s" %(e.code)

        self.lastCheck = rfc822.formatdate()

        num_notifications = len(timeline)

        if num_notifications > MAX_NOTIFICATIONS:
            if self.debug:
                print "%s new tweets\n" %(num_notifications)
            self.NotifyNum(num_notifications)
        elif num_notifications < 0:
            if self.debug:
                print "no new tweets\n"
        else:
            for msg in timeline:
                id = msg.GetId()
                created = msg.GetCreatedAt()
                relative_created = msg.GetRelativeCreatedAt()
                name = msg.GetUser().name
                screen_name = msg.GetUser().screen_name
                text = self.unescape(msg.GetText())
                url = "http://twitter.com/"+screen_name+"/statuses/"+str(id)

                if self.debug:
                    print "user: %s (%s)\nmsg: %s\nurl: %s\n" %(name, created, text, url)
                self.Notify(id, created, relative_created, name, screen_name, text)

        gobject.timeout_add(self.interval,self._check)

if __name__ == '__main__':

    #DBusGMainLoop(set_as_default=True)

    public_only = False
    try:
        try:
            opts, args = getopt.getopt(
                sys.argv[1:],
                "hp",
                ["help", "public"])
        except getopt.GetoptError:
            raise Usage()

        for o, a in opts:
            if o in ("-h", "--help"):
                raise Usage('help')
            elif o in ("-p", "--public"):
                public_only = True
            else:
                raise Usage()
    except Usage, err:
        print >> sys.stderr, err.msg
        sys.exit(2)

    t = TwitterCheck(public_only)
    try:
        loop = gobject.MainLoop()
        loop.run()
    except KeyboardInterrupt:
        print "twittercheck shut down..."
    except Exception, ex:
        print "Exception in twittercheck: %s" %(ex)

