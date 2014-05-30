# coding: utf-8
from lib.PyGtalkRobot import GtalkRobot, xmpp
from BomNegocio import *

try:
	from local_conf import user, pasw
except ImportError:
	user = None
	pasw = None
	
class BomNegocioBot(GtalkRobot):
	
	def __init__(self, **kwargs):
		GtalkRobot.__init__(self, **kwargs)
		self.b = BomNegocio(BomNegocio.RJ, BomNegocio.INSTRUMENTOS_MUSICAIS)
		
	def command_003_search(self, user, msg, args):
		"""(search)( +(.*))?$(?i)"""
		responses=self.b.find(q=args[1]).sort().get_response()[:5]
		message=[]
		## Lista apenas os 5 primeiros recuperados::
		for r in responses:
			message.append( "Titulo: {0} - Preço: {1}\nLink: {2}".format(r['title'].encode('utf-8').strip(), r['price'], r['url']) )
		message = "\n\n".join(message)
		self.replyMessage(user, message)
			
if __name__ == '__main__':
	bot = BomNegocioBot()
	bot.setState('available', "TestBot")
	bot.start(user, pasw)