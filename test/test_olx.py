# coding: utf-8
from os import path
PROJECT_ROOT = path.abspath(path.dirname(__file__))

import unittest
import responses
from nose.tools import assert_equals
from Olx import OlxApi, CITY_OLX, CATEGORY_OLX, query_string


class MockResponse(object):

    def __init__(self, file_test):
        self.file_test = path.join(PROJECT_ROOT, file_test)

    def __str__(self):
        handle = open(self.file_test)
        html = "".join(handle)
        return html


class TestOlx(unittest.TestCase):

    def setUp(self):
        pass

    def test_1(self):
        """
            Caso a cidade seja RJ e a categoria instrumentos-musicais,
            a url http://rj.bomnegocio.com/instrumentos-musicais, deve
            ser gerada
        """
        o = OlxApi(CITY_OLX.RJ, CATEGORY_OLX.INSTRUMENTOS_MUSICAIS)
        assert_equals(o.url, 'http://rj.olx.com.br/instrumentos-musicais')

    def test_2(self):
        """
            Caso a proprieda url seja invocada, ela deve recuperar
            o serviço que esta sendo utilizado.
        """
        o = OlxApi(CITY_OLX.RJ, CATEGORY_OLX.IMOVEIS)
        assert_equals(o.url, 'http://rj.olx.com.br/imoveis')

    @responses.activate
    def test_3(self):
        """
            Quando o metodo find for invocaod, deve realizar uma busca
            e recupera a primeira pagina de imoveis.
        """
        body = MockResponse('imoveis-list.html')
        o = OlxApi(CITY_OLX.RJ, CATEGORY_OLX.IMOVEIS)
        url = "{0}?q={1}".format(o.url, "Casa")
        responses.add(
            responses.GET, url, body=body, status=200, match_querystring=True)

        find = o.find(q="Casa").response
        assert_equals(len(find), 50)
        title = u'VENDO OU TROCO - Casa em estado de primeira loca\xe7\xe3o em ponta negra'
        assert_equals(find[0]['title'], title)
        assert_equals(find[0]['price'], u'R$ 265.000')

    @responses.activate
    def test_4(self):
        """
            Caso o parâmetro 'q' possua uma palavra chave ele deve realizar
            uma busca pela palavra.
        """
        body = MockResponse('baixo_trb.html')
        o = OlxApi(CITY_OLX.RJ, CATEGORY_OLX.INSTRUMENTOS_MUSICAIS)
        url = "{0}?q={1}".format(o.url, "yamaha trb")
        responses.add(
            responses.GET, url, body=body, status=200, match_querystring=True)

        find = o.find(q="yamaha trb").response
        assert_equals(len(find), 4)
        assert_equals(find[0]['title'], 'Baixo yamaha trb-4p')
        assert_equals(find[0]['price'], 'R$ 5.000')

    def test_5(self):
        """
            Caso parâmetro seja passado, o decorador query_string
            deve definir a url default do serviço.
        """
        class OlChis(OlxApi):
            @query_string
            def call_me(self, q):
                return q
        m = OlChis(CITY_OLX.RJ, CATEGORY_OLX.INSTRUMENTOS_MUSICAIS)
        url = "http://rj.olx.com.br/instrumentos-musicais?q={}"
        assert_equals(m.call_me(q="yamaha trb"), url.format("yamaha+trb"))
        assert_equals(m.call_me(q="fender"), url.format("fender"))
        assert_equals(m.call_me(q="açai"), url.format("açai"))
        assert_equals(m.call_me("carro"), url.format("carro"))
