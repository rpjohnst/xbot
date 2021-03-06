# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import random
from userlevelHandler import getLevel
from securityHandler import isAllowed
import re
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 100
    def action(self, complete):
        msg=complete.message()
	kickee = msg.split()[0]
        kickMessage=' '.join(msg.split()[1:])
	if kickMessage=="":
	    kickMessage="Go away."
        print "kickee", kickee, "user", complete.user(), "allowed", isAllowed(complete.userMask()), "cmd/level", complete.cmd()[0], getLevel(complete.cmd()[0])
        if kickee == '$U$' or kickee == complete.user() or isAllowed(complete.userMask())>=getLevel('kick'):
            toKick=["KICK $C$ "+kickee+" :"+kickMessage]
            return toKick
        else:
            return ["PRIVMSG $C$ :ACTION kicks "+kickee+" in the shin (%s)"%kickMessage]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !kick module","PRIVMSG $C$ :Usage: (Requires Elevated Bot Privileges)","PRIVMSG $C$ :!kick [user]"]
