# -*- coding: utf-8 -*-
#!/usr/bin/python
import urllib2
import re

class SMFThread(object):
    def __init__(self, threadURL):
        self.threadURL=threadURL
        self.postID=threadURL.split('#')
        if len(self.postID)==1:
            self.postID=None
        else:
            self.postID=self.postID[-1]
        page=urllib2.urlopen(threadURL).read()
        thread={}
        thread['entries']=[]
        thread['page']={}
        thread['thread']={}
        thread['entriesByID']={}
        thread['thread']['url']=threadURL
        thread['thread']['title']=re.findall("<title>(.*?)</title>", page)[0]
        posts=re.findall("<div class=\"post\">(.*?)</div>", page)
        postLinks=re.findall("<td valign=\"middle\">\s*<a href=\"(.*?)\">\s*<img", page)
        users=re.findall("title=\"View the profile of (.*?)\"", page)
        pages=re.findall("<a class=\"navPages\" href=\"(.*?)\">(.*?)</a>", page)
        linkTree=re.findall("<div id=\"linktree\">(.*?)</div>",page, re.DOTALL)[0]
        linkTree=re.sub("</?a.*?>","", linkTree)
        thread['thread']['linktree']=linkTree.split(' < ')[:-1]
        currentpage=re.findall("\[<b>([0-9]*?)</b>\]", page)[0]
        for index, post in enumerate(posts):
            post=re.sub("<\s*br\s*/?>","\n",post)
            post=re.sub("<\s*b\s*>(.*?)<\s*/b\s*>","\x03b\g<1>\x03b",post)
            post=re.sub("<\s*i\s*>(.*?)<\s*/i\s*>","\x03i\g<1>\x03i",post)
            post=re.sub("<\s*u\s*>(.*?)<\s*/u\s*>","\x03u\g<1>\x03u",post)
            post=re.sub("<.*?>","",post)
            posts[index]=post
        for index, _ in enumerate(posts):
            thread['entries'].append({'name':users[index].strip(), 'post':posts[index], 'url':postLinks[index], 'id':postLinks[index].split('#')[-1]})
            thread['entriesByID'][postLinks[index].split('#')[-1]]=thread['entries'][-1]
        thread['thread']['posts']=len(thread['entries'])
        thread['page']['current']=currentpage
        thread['page']['pages']={}
        thread['page']['pages'][int(currentpage)]=threadURL
        for url, number in pages:
            thread['page']['pages'][int(number)]=url
        thread['page']['max']=sorted(thread['page']['pages'].keys())[-1]
        self.thread=thread

if __name__=="__main__":
    thread=SMFThread("http://forum.metroidconstruction.com/index.php/topic,638.msg10122.html#msg10122")
    print "Indicated Post in",thread.thread['thread']['title'], "(of",thread.thread['thread']['posts'],"posts)"
    print "in", thread.thread['thread']['linktree'][-1]
    print "by",thread.thread['entriesByID'][thread.postID]['name']
    print thread.thread['entriesByID'][thread.postID]['post']
    print thread.thread['entriesByID'][thread.postID]['url']
    print thread.thread['entriesByID'][thread.postID]['id']
    print "Current page is",thread.thread['page']['current'],"of", thread.thread['page']['max']
    print "Links to pages are", thread.thread['page']['pages']
    #print "The OP was"
    #firstPageOfThread=SMFThread(thread.thread['page']['pages'][1])
    #print firstPageOfThread.thread['entries'][0]['post']
    #print "By",firstPageOfThread.thread['entries'][0]['name']
