# coding: utf-8
import unittest
from mock import patch, Mock
from nose.tools import assert_true, assert_equals
from BomNegocio import *

class MockUrllib(Mock):

	def __init__(self, file_test):
		self.file_test = file_test

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
	
	@patch('BomNegocio.urllib2.urlopen')
	def test_quando_o_metodo_find_for_chamado_deve_realizar_uma_busca_e_recupera_a_primeira_pagina_de_imoveis(self, url):
		url.return_value = MockUrllib('imoveis-list.html')
		b = BomNegocio(BomNegocio.RJ, BomNegocio.IMOVEIS)
		find = b.find();
		assert_equals(len(find), 50)
		assert_equals(find[0]['title'], u'Casa Itaipua\xe7u Carnaval10 m praia piscina/Churrasq')
		assert_equals(find[0]['price'], u'R$ 3.000')
		
	@patch('BomNegocio.urllib2.urlopen')
	def test_quando_o_metodo_find_for_chamado_deve_realizar_uma_busca_e_recupera_a_primeira_pagina_instrumentos(self, url):
		url.return_value = MockUrllib('intrumentos-list.html')
		b = BomNegocio(BomNegocio.RJ, BomNegocio.INSTRUMENTOS_MUSICAIS)
		find = b.find();
		assert_equals(len(find), 50)
		assert_equals(find[0]['title'], u'Bateria turbo power')	
		assert_equals(find[0]['price'], u'R$ 900')
		
	@patch('BomNegocio.urllib2.urlopen')
	def test_caso_o_parametro_Q_possua_uma_palavra_chave_ele_deve_realizar_uma_busca_pela_palavra(self ,url):
		url.return_value = MockUrllib('busca_trb.html')
		b = BomNegocio(BomNegocio.RJ, BomNegocio.INSTRUMENTOS_MUSICAIS)
		find = b.find(q='yamaha trb');
		assert_equals(len(find), 3)
		assert_equals(b.query, 'yamaha+trb')
		assert_equals(find[0]['title'], u'Baixo Yamaha TRB 1005 zero')
		assert_equals(find[0]['price'], u'R$ 3.500')
	