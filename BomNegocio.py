# coding: utf-8
import urllib
from bs4 import BeautifulSoup

class BomNegocio(object):
	RJ="rio_de_janeiro"
	INSTRUMENTOS_MUSICAIS="instrumentos_musicais"
	IMOVEIS='imoveis'
	
	def __init__(self, contry, type):
		self.contry = contry
		self.type = type
	
	@property	
	def url(self):
		return 'http://www.bomnegocio.com/%s/%s' % (self.contry, self.type)	
	
	def _query(func):
		"""
			Antes que o método find seja invocado, o decorador verifica 
			se a variavel 'q' possui algum valor definido::
		"""
		def wrap(self, *arg, **kwargs):
			if kwargs.get('q') is not None:
				self.query=kwargs.get('q').replace(' ', '+').strip()
				url="%s?q=%s" % (self.url, self.query)
			else:
				url=self.url
			return func(self, q=url)
		return wrap
		
	@_query
	def find(self, q=None):
		response = ();
		"""
			Método realiza busca das informações desejadas::
		"""
		html_bom_negocio = urllib.urlopen(q).read()
		soup = BeautifulSoup(html_bom_negocio)
		
		for li in soup.find_all('li', 'list_adsBN_item'):
			try:
				price = li.find('p', 'price').get_text().strip()
			except:
				price = '0,00'
			iten = {'title':li.h3.a.get_text(), 
					'price':price, 
					"publicated":li.find('div', 'col_4').get_text(), 
					"state":li.find('div', 'col_2').find('div', 'info').find_all('p','text')[0].get_text().strip(), 
					"type":li.find('div', 'col_2').find('div', 'info').find_all('p','text')[1].get_text().strip(), 
					"url":li.a['href']}
			response = response + (iten,)
			self.response=response
		return self
	
	def get_response(self):
		return self.response
	
	def sort(self, alg=None):
		reverse=alg=='price_max'
		def getKey(item):
			return item['price']
		self.response=sorted(self.response, key=getKey, reverse=reverse)
		return self

if __name__ == '__main__':
	bom = BomNegocio(BomNegocio.RJ, BomNegocio.INSTRUMENTOS_MUSICAIS)
	print bom.find(q='yamaha trb').get_response()