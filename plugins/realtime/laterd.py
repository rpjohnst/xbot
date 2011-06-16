# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import settingsHandler
from pluginArguments import pluginArguments
from pluginFormatter import formatOutput, formatInput
import time
def getMessage(id):
    return settingsHandler.readSetting("laterd","message",where="id='%s'"%id)
def getRecipient(id):
    return settingsHandler.readSetting("laterd","recipient",where="id='%s'"%id)
def getSender(id):
    return settingsHandler.readSetting("laterd","sender",where="id='%s'"%id)
def getSenderMask(id):
    return settingsHandler.readSetting("laterd","senderMask",where="id='%s'"%id)
def getTimestamp(id):
    return settingsHandler.readSetting("laterd","timestamp",where="id='%s'"%id)
def getAnonymous(id):
    return settingsHandler.readSetting("laterd","anonymous",where="id='%s'"%id)=="1"
def correctChannel(id, channel):
    messageChannel=settingsHandler.readSetting("laterd", "channel", where="id='%s'"%id)
    return (channel.lower() in [messageC.lower() for messageC in messageChannel.split('|')] or messageChannel=="")
def setMessageSent(id):
    print "Attempting to set complete"
    settingsHandler.updateSetting("laterd", "sent", "1", where="id='%s'"%id)
    print "Set complete!"
class pluginClass(plugin):
    def gettype(self):
        return "realtime"
    def __init_db_tables__(self, name):
        settingsHandler.newTable("laterd", "id", "recipient","sender","senderMask","timestamp","message", "channel", "anonymous",  "sent")
    def action(self, complete):
        user=complete.user()
        if complete.type()!="PRIVMSG":
            return [""]
        returns=[]
        messages=settingsHandler.readSettingRaw("laterd","id",where="('"+user.lower()+"' GLOB recipient OR recipient GLOB '*|"+user.lower()+"|*') AND sent='0'")
        if messages!=[]:
            for message in messages:
                wipeMessage=True

                messageID=str(message[0])
                try:
                    sender=getSender(messageID)
                    senderMask=getSenderMask(messageID)
                    timestamp=getTimestamp(messageID)
                    messageText=getMessage(messageID)
                    plugin=messageText.split()[0]
                    if not correctChannel(messageID, complete.channel()):
                        continue
                    if plugin in globalv.loadedPlugins.keys():
                        arguments=pluginArguments(':'+senderMask+" PRIVMSG "+complete.channel()+" :!"+messageText.replace('$recipient$', user).replace('$*$', complete.fullMessage()))
                        arguments=formatInput(arguments)
                        message=globalv.loadedPlugins[plugin].action(arguments)
                        if message in [[],[""]]:
                            wipeMessage=False
                        #returns+=[m.decode('utf-8') for m in message]
                        returns+=message
                        if message!=[""] and message!=[]:
                            msg=message[0]
                            if msg.split()[0]=="PRIVMSG" or msg.split()[0]=="NOTICE":
                                location=msg.split()[1]
                            else:
                                location="$C$"
                            if not getAnonymous(messageID):
                                returns.append("PRIVMSG "+location+" :From "+sender+" to "+user+" at "+time.strftime("%H:%M on %d-%m-%Y",time.gmtime(int(timestamp))))
                        if wipeMessage:
                            setMessageSent(messageID)
                    else:
                        returns.append("PRIVMSG $C$ :"+messageText)
                        if not getAnonymous(messageID):
                            returns.append("PRIVMSG $C$ :From "+sender+" to "+user+" at "+time.strftime("%H:%M on %d-%m-%Y",time.gmtime(int(timestamp))))
                        setMessageSent(messageID)
                except Exception as detail:
                    print "There was an error in one of the later messages:",detail
                    setMessageSent(messageID)

        return returns
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]