#
# THIS FILE IS PART OF THE MUMBLES PROJECT AND IS LICENSED UNDER THE GPL.
# SEE THE 'COPYING' FILE FOR DETAILS
#
# Simple Growl Network Server Plugin
#
#------------------------------------------------------------------------

from mumbles.MumblesPlugin import *
import dbus
import sys,os,string,re,glob

def parseMessage(message):

        program =  None
        newMessage = []
        path = ""
        words = message.split()
        for word in words:
            http = re.compile("http")
            www = re.compile("www.")
            volumes = re.compile("/Volumes/")
            network = re.compile("/Network/")
            mov = re.compile(".mov")

            if (http.match( word ) or www.match(word)  and program == None):
                program = "firefox"
                path = word
            elif (volumes.match(word) or  network.match(word) and program == None):
                path = word
                if (mov.match(word)):
                    program = "djv"
                    ## this doesent work yet.... weird...

                else:
                    program = "konqueror"
                newWord = os.path.basename(word)
                if (newWord == ""):
                    word = word
                else:
                    word = newWord
            newMessage.append(word)

        mesg = ' '.join(newMessage)
        return mesg,program,path


class GrowlMumbles(MumblesPlugin):

    plugin_name = "GrowlMumbler"

    dbus_interface = "info.growl.Growl"
    dbus_path = "/info/growl/Growl"
    icons = {'growl' : 'growl.png'}

    __message = None
    __app = None
    __path = None

    def __init__(self, mumbles_notify, session_bus):
        self.signal_config = {
            "Notify": self.Notify
        }

        MumblesPlugin.__init__(self, mumbles_notify, session_bus)
        #self.add_click_handler(self.onClick)

    def Notify(self, title, message):
        icon = self.get_icon('growl')
        (message,app,path) = parseMessage(message)
        self.__message = message
        self.__app = app
        self.__path = path
        if (self.__app != None):
            self.add_click_handler(self.onClick)

        self.mumbles_notify.alert(self.plugin_name, title, message, icon)

    def onClick(self, widget, event, plugin_name):
         if event.button == 3:
             self.mumbles_notify.close(widget.window)
         else:
             self.open_uri(self.__path, self.__app)

    def open_uri(self, path, app):
        #mime_type = gnomevfs.get_mime_type(uri)
        #application = gnomevfs.mime_get_default_application(mime_type)
        os.system(app + ' "' + path + '" &')

