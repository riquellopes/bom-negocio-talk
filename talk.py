#!/usr/bin/python
"""
	A lib funciona da seguinte forma, as regex devem ser escritas como um
	comentario, e o metodo deve possui o prefixo command_::
"""
from lib.PyGtalkRobot import GtalkRobot, xmpp

class BomNegocioBot(GtalkRobot):
	
	def command_003_search(self, user, msg, args):
		"""(search|s)( +(.*))?$(?i)"""
		print args
		self.replyMessage(user, "http://gmail.com")
	
	def sendFile(path=None):
		ibb=xmpp.filetransfer.IBB()
		ibb.PlugIn(self.conn)
		with file(path) as _file:
			ibb.OpenStream('Nome', "email", _file)
			
if __name__ == '__main__':
	bot = BomNegocioBot()
	bot.setState('available', "TestBot")
	bot.start("riquellopes@gmail.com", "052020266")