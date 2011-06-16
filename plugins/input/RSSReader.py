# -*- coding: utf-8 -*-
from plugins import plugin
import time
from bitlyServ import bitly
import feedparser
import globalv
class asyncInput(object):
    def __init__(self,Queue,stop,feedName, channel, name):
        self.Queue=Queue
        colour="\x03"
        print "Hello, I am feedreader",name," and I am feedreading",feedName
        self.Queue.put("#PRIVMSG %s :%s started up successfully\r\n"%(channel, name))
        latestFeedItem=""
        secondLatestFeedItem=""
        if feedName.startswith("http://"):
            feedName=feedName[7:]
        checkFrequencies=[10,20,30,60,120,180,240,300]
        lastReadWasBlank=0
        feed=feedparser.parse("http://"+feedName)
        latestFeedItem=feed.entries[0].id
        checkFrequency=3
        while stop.isSet()==False:
            try:
                feed=feedparser.parse("http://"+feedName)
                newFeedItem=feed.entries[0].id
                newItems=[]
                if newFeedItem!=latestFeedItem and newFeedItem!=secondLatestFeedItem:
                    iterateBack=0
                    while (feed.entries[iterateBack].id!=latestFeedItem and iterateBack<len(feed.entries)-1 and iterateBack < 5):
                        newItems.append ((feed.entries[iterateBack].link, feed.entries[iterateBack].title))
                        iterateBack+=1
                    secondLatestFeedItem=latestFeedItem
                    latestFeedItem=newFeedItem
                    for item in newItems:
                        Queue.put("#PRIVMSG "+channel+" :\x0312"+name+"\x03:\x0311 "+item[1]+"\x03 (at \x0312"+(item[0] if len(item[0])<20 else bitly(item[0]))+"\x03)\r\n")
                    if checkFrequency>0:
                        checkFrequency-=len(newItems)
                        checkFrequency=0 if checkFrequency<0 else checkFrequency
                        print "Got a lot of items that time. Upping check frequency to",checkFrequencies[checkFrequency],"seconds."
                    
                if len(newItems)==0:
                    if checkFrequency<len(checkFrequencies)-1 and lastReadWasBlank:
                        checkFrequency+=1
                        lastReadWasBlank=0
                        print "Nothing this iteration. Dropping check frequency to",checkFrequencies[checkFrequency],"seconds."
                    lastReadWasBlank=1
                time.sleep(checkFrequencies[checkFrequency])
            except Exception as detail:
                print "RSS Grabbing failure! Bad feed?"
                time.sleep(60)
        Queue.put("#PRIVMSG "+channel+" :RSS Reader "+name+" Shut down.\r\n")
    def gettype(self):
        return "input"
    def describe(self, complete):
        return ["PRIVMSG $C$ :I watch RSS feeds and talk about new entries!"]