# -*- coding: utf-8 -*-
from plugins import pluginfrom settingsHandler import readSettingimport globalvclass pluginClass(plugin):	def gettype(self):		return "command"	def action(self, complete):		return ["PRIVMSG NickServ :IDENTIFY "+readSetting("core","password")]	def describe(self, complete):		return ["PRIVMSG $C$ :I am the !opYourself module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!opYourself"]