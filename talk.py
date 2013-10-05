#!/usr/bin/python
"""
	A lib funciona da seguinte forma, as regex devem ser escritas como um
	comentario, e o metodo deve possui o prefixo command_::
"""
from lib.PyGtalkRobot import GtalkRobot, xmpp
from BomNegocio import *

class BomNegocioBot(GtalkRobot):
	
	def __init__(self, **kwargs):
		GtalkRobot.__init__(self, **kwargs)
		self.b = BomNegocio(BomNegocio.RJ, BomNegocio.INSTRUMENTOS_MUSICAIS)
		
	def command_003_search(self, user, msg, args):
		"""(search)( +(.*))?$(?i)"""
		response = self.b.find(q=args[1]).sort()
		print len(response.get_response())
		self.replyMessage(user, "http://gmail.com")
	
#	def sendFile(path=None):
#		ibb=xmpp.filetransfer.IBB()
#		ibb.PlugIn(self.conn)
#		with file(path) as _file:
#			ibb.OpenStream('Nome', "email", _file)
			
if __name__ == '__main__':
	bot = BomNegocioBot()
	bot.setState('available', "TestBot")
	bot.start("riquellopes@gmail.com", "052020266")