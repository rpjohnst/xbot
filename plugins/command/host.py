# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message()
        if msg in globalv.nicks.keys():
            return ["PRIVMSG $C$ :"+globalv.nicks[msg]]
        return ["PRIVMSG $C$ :Unknown User"]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
