# coding: utf-8
from os import path
PROJECT_ROOT = path.abspath( path.dirname(__file__) )

import unittest
from mock import patch, Mock
from nose.tools import assert_true, assert_equals
from BomNegocio import *

class MockUrllib(object):
	
	def __init__(self, file_test):
		self.file_test = path.join(PROJECT_ROOT, file_test)

	def read(self):
		handle = open(self.file_test)
		html = "".join( handle )
		return html
		
class BomNegocioTest(unittest.TestCase):
	
	def test_estado_RJ_e_tipo_instrumentos_musicais_deve_geral_url(self):
		b = BomNegocio(BomNegocio.RJ, BomNegocio.INSTRUMENTOS_MUSICAIS)
		assert_equals(b.url, 'http://www.bomnegocio.com/rio_de_janeiro/instrumentos_musicais')
	
	def test_estado_RJ_e_tipo_imoveis_deve_geral_url(self):
		b = BomNegocio(BomNegocio.RJ, BomNegocio.IMOVEIS)
		assert_equals(b.url, 'http://www.bomnegocio.com/rio_de_janeiro/imoveis')
	
	@patch('BomNegocio.urllib.urlopen')
	def test_quando_o_metodo_find_for_chamado_deve_realizar_uma_busca_e_recupera_a_primeira_pagina_de_imoveis(self, url):
		url.return_value = MockUrllib('imoveis-list.html')
		b = BomNegocio(BomNegocio.RJ, BomNegocio.IMOVEIS)
		find = b.find().get_response()
		assert_equals(len(find), 50)
		assert_equals(find[0]['title'], u'Casa Itaipua\xe7u Carnaval10 m praia piscina/Churrasq')
		assert_equals(find[0]['price'], u'R$ 3.000')
		
	@patch('BomNegocio.urllib.urlopen')
	def test_quando_o_metodo_find_for_chamado_deve_realizar_uma_busca_e_recupera_a_primeira_pagina_instrumentos(self, url):
		url.return_value = MockUrllib('intrumentos-list.html')
		b = BomNegocio(BomNegocio.RJ, BomNegocio.INSTRUMENTOS_MUSICAIS)
		find = b.find().get_response()
		assert_equals(len(find), 50)
		assert_equals(find[0]['title'], u'Bateria turbo power')	
		assert_equals(find[0]['price'], u'R$ 900')
		
	@patch('BomNegocio.urllib.urlopen')
	def test_caso_o_parametro_Q_possua_uma_palavra_chave_ele_deve_realizar_uma_busca_pela_palavra(self ,url):
		url.return_value = MockUrllib('baixo_trb.html')
		b = BomNegocio(BomNegocio.RJ, BomNegocio.INSTRUMENTOS_MUSICAIS)
		find = b.find(q='yamaha trb').get_response()
		assert_equals(len(find), 2)
		assert_equals(b.query, 'yamaha+trb')
		assert_equals(find[0]['title'], u'Baixo cort b5 opn')
		assert_equals(find[0]['price'], u'R$ 1.300')
	
	@patch('BomNegocio.urllib.urlopen')
	def test_o_resultado_recuperado_pode_ser_reorndenado(self ,url):
		url.return_value = MockUrllib('busca_trb.html')
		b = BomNegocio(BomNegocio.RJ, BomNegocio.INSTRUMENTOS_MUSICAIS)
		find = b.find(q='yamaha trb').sort('price_max').get_response()
		assert_equals(len(find), 3)
		
		assert_equals(b.query, 'yamaha+trb')
		assert_equals(find[0]['title'], u'Baixo Yamaha Trb 5i Slap cut.mesmo pre to trb jp1')
		assert_equals(find[0]['price'], u'R$ 4.800')
		
		response = b.sort('price_mim').get_response()
		assert_equals(response[0]['title'], u'Baixo JB - S. Martyn- Fender Samarium Noiselles C')
		assert_equals(response[0]['price'], u'R$ 3.200')
		
	