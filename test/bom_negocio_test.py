# coding: utf-8
from os import path
PROJECT_ROOT = path.abspath( path.dirname(__file__) )

import unittest
from mock import patch, Mock
from nose.tools import assert_true, assert_equals, assert_raises
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
		b = BomNegocio(BOM_NEGOCIO_CIDADE.RJ, BOM_NEGOCIO_CATEGORIA.INSTRUMENTOS_MUSICAIS)
		assert_equals(b.url, 'http://rj.bomnegocio.com/instrumentos-musicais')
	
	def test_estado_RJ_e_tipo_imoveis_deve_geral_url(self):
		b = BomNegocio(BOM_NEGOCIO_CIDADE.RJ, BOM_NEGOCIO_CATEGORIA.IMOVEIS)
		assert_equals(b.url, 'http://rj.bomnegocio.com/imoveis')
	
	@patch('BomNegocio.urllib.urlopen')
	def test_quando_o_metodo_find_for_chamado_deve_realizar_uma_busca_e_recupera_a_primeira_pagina_de_imoveis(self, url):
		url.return_value = MockUrllib('imoveis-list.html')
		b = BomNegocio(BOM_NEGOCIO_CIDADE.RJ, BOM_NEGOCIO_CATEGORIA.IMOVEIS)
		find = b.find(q="Casa").get_response()
		assert_equals(len(find), 50)
		assert_equals(find[0]['title'], u'Casa Itaipua\xe7u Carnaval10 m praia piscina/Churrasq')
		assert_equals(find[0]['price'], u'R$ 3.000')
		
	@patch('BomNegocio.urllib.urlopen')
	def test_quando_o_metodo_find_for_chamado_deve_realizar_uma_busca_e_recupera_a_primeira_pagina_instrumentos(self, url):
		url.return_value = MockUrllib('intrumentos-list.html')
		b = BomNegocio(BOM_NEGOCIO_CIDADE.RJ, BOM_NEGOCIO_CATEGORIA.INSTRUMENTOS_MUSICAIS)
		find = b.find(q="Bateria").get_response()
		assert_equals(len(find), 50)
		assert_equals(find[0]['title'], u'Bateria turbo power')	
		assert_equals(find[0]['price'], u'R$ 900')
		
	@patch('BomNegocio.urllib.urlopen')
	def test_caso_o_parametro_Q_possua_uma_palavra_chave_ele_deve_realizar_uma_busca_pela_palavra(self ,url):
		url.return_value = MockUrllib('baixo_trb.html')
		b = BomNegocio(BOM_NEGOCIO_CIDADE.RJ, BOM_NEGOCIO_CATEGORIA.INSTRUMENTOS_MUSICAIS)
		find = b.find(q='yamaha trb').get_response()
		assert_equals(len(find), 2)
		assert_equals(b.query, 'yamaha+trb')
		assert_equals(find[0]['title'], u'Baixo cort b5 opn')
		assert_equals(find[0]['price'], u'R$ 1.300')
	
	@patch('BomNegocio.urllib.urlopen')
	def test_o_resultado_recuperado_pode_ser_reorndenado(self ,url):
		url.return_value = MockUrllib('busca_trb.html')
		b = BomNegocio(BOM_NEGOCIO_CIDADE.RJ, BOM_NEGOCIO_CATEGORIA.INSTRUMENTOS_MUSICAIS)
		find = b.find(q='yamaha trb').sort('price_max').get_response()
		assert_equals(len(find), 3)
		
		assert_equals(b.query, 'yamaha+trb')
		assert_equals(find[0]['title'], u'Baixo Yamaha Trb 5i Slap cut.mesmo pre to trb jp1')
		assert_equals(find[0]['price'], u'R$ 4.800')
		
		response = b.sort('price_mim').get_response()
		assert_equals(response[0]['title'], u'Baixo JB - S. Martyn- Fender Samarium Noiselles C')
		assert_equals(response[0]['price'], u'R$ 3.200')
	
	def test_o_decoretor_query_deve_modificar_o_yamaha_trb_para_uma_url_valida_para_o_bom_negocio(self):	
		class Mock(BomNegocio):
			
			@query_string
			def call_me(self, q):
				return q
		
		m = Mock(BOM_NEGOCIO_CIDADE.RJ, BOM_NEGOCIO_CATEGORIA.INSTRUMENTOS_MUSICAIS)		
		assert_equals(m.call_me(q="yamaha trb"), "http://rj.bomnegocio.com/instrumentos-musicais?q=yamaha+trb")
		assert_equals(m.call_me(q="fender"), "http://rj.bomnegocio.com/instrumentos-musicais?q=fender")
		assert_equals(m.call_me(q="açai"), "http://rj.bomnegocio.com/instrumentos-musicais?q=açai")
		assert_equals(m.call_me("carro"), "http://rj.bomnegocio.com/instrumentos-musicais?q=carro")
	
	def test_caso_nenhuma_parametro_seja_passado_para_o_metodo_de_find_uma_exception_deve_ser_levantada(self):
		with assert_raises(BomNegocioException):
			b = BomNegocio(BOM_NEGOCIO_CIDADE.RJ, BOM_NEGOCIO_CATEGORIA.INSTRUMENTOS_MUSICAIS)
			b.find()