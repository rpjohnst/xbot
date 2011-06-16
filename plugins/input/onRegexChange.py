# -*- coding: utf-8 -*-
from plugins import plugin
import time
import globalv
import re
import urllib2
class asyncInput(object):
    def __init__(self,Queue,stop, channel, name, url, regex):
        self.Queue=Queue
        latestFeedItem=""
        checkFrequencies=[10,20,30,60,120,180,240,300,600,1200,3600]
        print "Starting up onRegexChange for",url,"looking for",regex
        lastReadWasBlank=0
        checkFrequency=3
        while stop.isSet()==False:
            try:
                feed=urllib2.urlopen(url).read()
                try:
                    newFeedItem=re.findall(regex,feed.replace('\n','').replace('\r',''))[0]
                except:
                    print "Failed to find new entry. Rolling with the old one"
                    print re.findall(regex,feed.replace('\n','').replace('\r',''))
                    newFeedItem=latestFeedItem
                if newFeedItem!=latestFeedItem:
                    try:
                        float(newFeedItem)
                        float(latestFeedItem)
                        areInts=True
                    except: 
                        areInts=False
                    if areInts:
                        if newFeedItem>latestFeedItem:
                            direction=" (increasing)"
                        else:
                            direction=" (decreasing)"
                    else:
                        direction=""
                    latestFeedItem=newFeedItem
                    Queue.put("#PRIVMSG "+channel+" :\x0312"+name+"\x03: \x0311"+newFeedItem+direction+"\r\n") 
                    if checkFrequency>0:
                        checkFrequency-=1
                        checkFrequency=0 if checkFrequency<0 else checkFrequency
                else:
                    if checkFrequency<len(checkFrequencies)-1 and lastReadWasBlank:
                        checkFrequency+=1
                        lastReadWasBlank=0
                    lastReadWasBlank=1
                time.sleep(checkFrequencies[checkFrequency])
            except Exception as detail:
                print "Regex Grabbing failure! Bad feed?"
                Queue.put("#PRIVMSG PY :"+name+" shutting down: "+str(detail)+"\r\n")
                stop.set()
        Queue.put("#PRIVMSG "+channel+" :Site Reader "+name+" Shut down.\r\n")
    def gettype(self):
        return "input"
    def describe(self, complete):
        return ["PRIVMSG $C$ :I watch RSS feeds and talk about new entries!"]