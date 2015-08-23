# coding: utf-8

import unittest
import responses
from nose.tools import assert_raises
from Olx import OlxApi, CITY_OLX, CATEGORY_OLX, OlxException


class TestStatus(unittest.TestCase):

    def setUp(self):
        self.api = OlxApi(CITY_OLX.RJ, CATEGORY_OLX.INSTRUMENTOS_MUSICAIS)

    @responses.activate
    def test_1(self):
        """
            Caso o status_code seja diferente de 200, uma exception deve
            ser levantada.
        """
        url = "http://rj.olx.com.br/instrumentos-musicais?q=yamaha+trb"
        responses.add(
            responses.GET, url, body='', status=544, match_querystring=True)
        assert_raises(OlxException, self.api.find, q='yamaha trb')
