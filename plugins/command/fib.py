# -*- coding: utf-8 -*-
from plugins import pluginimport globalvdef fib(num):	first = 0	second = 1	for i in range(num):		second = first + second		first = second - first	return firstclass pluginClass(plugin):	def gettype(self):		return "command"	def action(self, complete):		msg=complete.message()		fibs=[]		for i in range(0,int(msg)):			fibs.append(str(fib(i)))		print fibs		return ["PRIVMSG $C$ :"+', '.join(fibs)]	def describe(self, complete):		msg=complete.message()		sender=complete[0].split(' ')		sender=sender[2]		return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]