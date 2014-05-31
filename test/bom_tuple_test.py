# coding: utf-8
import unittest
from mock import patch, Mock
from nose.tools import assert_true, assert_equals, assert_raises
from BomNegocio import *

class BomTupleTest(unittest.TestCase):
	
	def test_os_parametros_que_forem_passados_deve_simular_propriedades_da_classe(self):
		b = BomList(RJ='rj', SP='sp')
		assert_equals(b.RJ, 'rj')
		assert_equals(b.SP, 'sp')
	
	def test_deve_ser_possuir_invocar_os_valores_utilizando_caixa_baixa(self):
		b = BomList(RJ='rj', SP='sp')
		assert_equals(b.rj, 'rj')
		assert_equals(b.sp, 'sp')
	
	def test_caso_uma_valor_nao_exista_uma_exception_deve_ser_chamada(self):
		b = BomList(RJ='rj', SP='sp')
		with assert_raises(IndexError):
			b.A