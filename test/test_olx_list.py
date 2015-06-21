# coding: utf-8

import unittest
from nose.tools import assert_equals, assert_raises
from olx import OlxList


class TestOlxList(unittest.TestCase):

    def test_1(self):
        """
            Os parâmetros que forem passados deve simiular um propriedade
            da classe.
        """
        b = OlxList('rj', 'sp')
        assert_equals(b.RJ, 'rj')
        assert_equals(b.SP, 'sp')

    def test_2(self):
        """
            Deve ser possivel invocar os valores utilizando caixa baixa
            ou alta.
        """
        b = OlxList(RJ='rj', SP='sp')
        assert_equals(b.rj, 'rj')
        assert_equals(b.sp, 'sp')

    def test_3(self):
        """
            Caso um valor não exista, uma exception deve ser levantada.
        """
        b = OlxList(RJ='rj', SP='sp')
        with assert_raises(IndexError):
            b.A

    def test_4(self):
        """
            Caso seja passado o valor joão e maria para OlxList, a chave
            JOAO_E_MARIA deve ser gerada e possuir o valor correspondente.
        """
        list = OlxList("joão e maria")
        assert_equals(list.JOAO_E_MARIA, 'joão e maria')
