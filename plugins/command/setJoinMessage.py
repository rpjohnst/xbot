# -*- coding: utf-8 -*-
from plugins import pluginimport globalv###NOT FIXING THIS. GODDAMN DATABASE IT.class pluginClass(plugin):	def gettype(self):		return "command"	def action(self, complete):		msg=complete.message()		if msg.split()[0]!="USER":			globalv.joinMessages[complete.channel()]=msg			with open("functions\\joinMessages.py","a") as cache:				cache.write("\nglobalv.joinMessages[\""+complete.channel()+"\"]=\""+msg+"\"")		else:			globalv.joinMessages[msg.split()[1].lower()]=' '.join(msg.split()[2:])			with open("functions\\joinMessages.py","a") as cache:				cache.write("\nglobalv.joinMessages[\""+msg.split()[1].lower()+"\"]=\""+' '.join(msg.split()[2:])+"\"")		return ["PRIVMSG $C$ :Ok!"]	def describe(self, complete):		return ["PRIVMSG $C$ :I am the !setJoinMessage module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [OPTIONAL \"USER\" FLAG] message"]