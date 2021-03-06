# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import settingsHandler
import time
from securityHandler import isAllowed
from userlevelHandler import getLevel
import re
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __append_seperator__(self):
        return True
    def action(self, complete):
        msg=complete.message()
        command=msg.split()[0]
        if command=="list":
            names=settingsHandler.readSettingRaw("laterd","recipient, sender, timestamp", where="sent='0' AND anonymous='0'")
            returns=[]
            for name in names:
                try:
                    recipient=name[0]
                    sender=name[1]
                    timestamp=name[2]
                    ctime=time.strftime("%H:%M on %d-%m-%Y",time.gmtime(int(timestamp)))
                    message=recipient+" has a message from "+sender+" (Sent on "+ctime+")"
                    returns.append(message)
                except:
                    pass
            if returns==[]:
                returns.append("No messages.")
            return ["PRIVMSG $C$ :"+', '.join(returns)]
        elif command=="remove":
            try:
                senderString=" and sender=='%s'"%complete.user()
                if isAllowed(complete.userMask())>=150:
                    senderString=""
                where  = "recipient=%s and sent='0'" % repr(msg.split()[1].lower())
                where += senderString
                print where
                settingsHandler.updateSetting("laterd","sent", "'2'", where=where)
                return ["PRIVMSG $C$ :Later successfully removed!"]
            except Exception as detail:
                return ["PRIVMSG $C$ :Later not removed"]
        else:
            anonymous = "0"
            secret_pfx = "secret::"
            if msg.startswith(secret_pfx):
                anonymous = "1"
                msg = msg[len(secret_pfx):]
            
            channels=[]
            while msg.split()[0][0]=="#":
                channels.append(msg.split()[0])
                msg=' '.join(msg.split()[1:])
            channel='|'.join(channels)
            recipients=list(set(msg.split()[0].lower().split(',')))
            recipients = [re.sub('[^0-9a-z-[\]*?]', '?', x) for x in recipients]
            sender=complete.user()
            senderMask=complete.userMask()
            timestamp=str(int(time.time()))
            message=' '.join(msg.split()[1:])
            message = message.replace('$U$','$recipient$')
            for recipient in recipients:
                print recipient
                id=str(int(settingsHandler.readSetting("laterd", "COUNT(id)"))+1)
                settingsHandler.writeSetting("laterd",["id", "recipient","sender","senderMask","timestamp","message", "channel", "anonymous",  "sent"],[id, recipient, sender, senderMask, timestamp, message, channel, anonymous, "0"])
                settingsHandler.db.commit()
            return ["PRIVMSG $C$ :Ok, I'll tell "+', '.join(recipients[:-1])+(" and "+recipients[-1] if len(recipients)>1 else recipients[-1])+" that when they next speak!"]
        return ["PRIVMSG $C$ :"+msg]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !later module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!later [recipient] [plugin to run (probably say or msg)] [arguments to plugin (What to say, mostly)]"]
