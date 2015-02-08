# -*- coding: utf-8 -*-
from plugins import plugin
import globalv,random
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message()
        colour="\x03"
        msg2=u''
        i=random.randint(3,12)

        try:
            msg = msg.decode('utf-8','replace')
        except:
            pass

        for letter in msg:
            msg2+=colour+str(i).rjust(2,"0")+letter
            i= i+1 if i<12 else 3
        result = "PRIVMSG $C$ :"+msg2+"\x03"
        return [result]
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
