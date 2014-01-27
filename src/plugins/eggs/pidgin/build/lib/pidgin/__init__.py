#
# THIS FILE IS PART OF THE MUMBLES PROJECT AND IS LICENSED UNDER THE GPL.
# SEE THE 'COPYING' FILE FOR DETAILS
#
# Pidgin Mumbles Plugin
#
#------------------------------------------------------------------------

from mumbles.MumblesPlugin import *
import dbus
import time
import re

class PidginMumbles(MumblesPlugin):

    plugin_name = "PidginMumbles"

    dbus_interface = "im.pidgin.purple.PurpleInterface"
    dbus_path = "/im/pidgin/purple/PurpleObject"

    dbus_name = "im.pidgin.purple.PurpleService"
    pidgin_interface = None
    

    icons = {'pidgin' : 'pidgin.png', 'irc' : 'irc.png'}

    def __init__(self, mumbles_notify, session_bus):
        self.signal_config = {
            "ReceivedImMsg": self.ReceivedImMsg,
            "ReceivedChatMsg": self.ReceivedChatMsg
        }

        MumblesPlugin.__init__(self, mumbles_notify, session_bus)
        self.FloodSuppressList = {}


    def SuppressMessage(self, msgFrom):
        messages = self.FloodSuppressList.get(msgFrom, [])
        messages.sort()
        now = time.time()
        if len(messages) >= 3:
            oldestMessage = messages.pop(0)
        else:
            oldestMessage = now
        messages.append(now)
        self.FloodSuppressList[msgFrom] = messages
        if len(messages) >= 3 and now - oldestMessage < 3:
            return True
        else:
            return False
        
        
    def ReceivedImMsg(self, account, name, message, conversation, flags):

        message = self.unescape(self.striphtml(message))
        icon = 0

        pidgin_object = self.session_bus.get_object(self.dbus_name, self.dbus_path)
        pidgin_interface = dbus.Interface(pidgin_object, self.dbus_interface)

        buddy = pidgin_interface.PurpleFindBuddy(account, name)
        if buddy != 0:
            name = pidgin_interface.PurpleBuddyGetAlias(buddy)

        name = self.unescape(name)
        
        if not self.SuppressMessage(name):
            icon = self.get_icon('pidgin')
            self.mumbles_notify.alert(self.plugin_name, name, message, icon)


    def ReceivedChatMsg(self, account, name, message, conversation, flags):

        message = self.unescape(self.striphtml(message))

        pidgin_object = self.session_bus.get_object(self.dbus_name, self.dbus_path)
        pidgin_interface = dbus.Interface(pidgin_object, self.dbus_interface)

        chatroom_name = pidgin_interface.PurpleConversationGetTitle(conversation)
        chat_data = pidgin_interface.PurpleConversationGetChatData(conversation)

        chat_nick = pidgin_interface.PurpleConvChatGetNick(chat_data)

        if name != chat_nick:
            name = chatroom_name+": "+name
        name = self.unescape(name)
        
        if not self.SuppressMessage(chatroom_name):
            icon = self.get_icon('irc')
            self.mumbles_notify.alert(self.plugin_name, name, message, icon)


    def striphtml(self, message):
        return re.compile('<[^>]+>').sub(' ',message)

    def unescape(self, s):
        s = s.replace("&lt;", "<")
        s = s.replace("&gt;", ">")
        s = s.replace("&apos;", "'")
        s = s.replace("&quot;", '"')
        # this has to be last:
        s = s.replace("&amp;", "&")
        return s

