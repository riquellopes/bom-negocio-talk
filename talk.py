# coding: utf-8
from lib.PyGtalkRobot import GtalkRobot, xmpp
from BomNegocio import *

class BomNegocioBot(GtalkRobot):
	
	def __init__(self, **kwargs):
		GtalkRobot.__init__(self, **kwargs)
		self.b = BomNegocio(BomNegocio.RJ, BomNegocio.INSTRUMENTOS_MUSICAIS)
		
	def command_003_search(self, user, msg, args):
		"""(search)( +(.*))?$(?i)"""
		responses=self.b.find(q=args[1]).sort().get_response()[:5]
		message=""
		## Lista apenas os 5 primeiros recuperados::
		for r in responses:
			message += "Preço: %s - Link: %s\n" % (r['price'], r['url'])
		print message
		self.replyMessage(user, message)
	
#	def sendFile(path=None):
#		ibb=xmpp.filetransfer.IBB()
#		ibb.PlugIn(self.conn)
#		with file(path) as _file:
#			ibb.OpenStream('Nome', "email", _file)
			
if __name__ == '__main__':
	bot = BomNegocioBot()
	bot.setState('available', "TestBot")
	bot.start("riquellopes@gmail.com", "052020266")