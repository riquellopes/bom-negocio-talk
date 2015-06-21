# coding: utf-8

import requests
from slugify import slugify
from functools import wraps
from bs4 import BeautifulSoup


class OlxException(Exception):
    pass


def query_string(func):
    """
        Antes que o método find seja invocado, o decorador verifica
        se a variavel 'q' possui algum valor definido.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            q = args[0]
        except IndexError:
            q = kwargs.get('q')

        if q is not None:
            self.query = q.replace(' ', '+').strip()
            url = "{0}?q={1}".format(self.url, self.query)
        else:
            url = self.url
        return func(self, q=url)
    return wrapper


class OlxList(list):

    def __init__(self, *args, **kwargs):
        for value in args:
            self.append({self._padronizar(value): value})

        for k in kwargs:
            self.append({k.upper(): kwargs[k]})

    def _padronizar(self, value):
        return slugify(value, separator='_').upper()

    def __getattr__(self, name):
        for l in self:
            try:
                return l[name.upper()]
            except KeyError:
                continue
        raise IndexError("")

CITY_OLX = OlxList(
    'rj',
    'sp',
    'rr',
    'am',
    'ac',
    'ro',
    'mt',
    'go',
    'to',
    'ba',
    'es',
    'se',
    'al',
    'rn',
    'pb',
    'ma',
    'pr',
)

CATEGORY_OLX = OlxList(
    INSTRUMENTOS_MUSICAIS='instrumentos-musicais',
    ANIMAIS_E_ACESSORIOS='animais-e-acessorios',
    BEBES_E_CRIANCAS='bebes-e-criancas',
    MODA_E_BELEZA='moda-e-beleza',
    PARA_SUA_CASA='para-a-sua-casa',
    ESPORTES='esportes',
    ELETRONICOS_E_CELULARES='eletronicos-e-celulares',
    IMOVEIS='imoveis',
    EMPREGOS_E_NEGOCIOS='empregos-e-negocios',
    VEICULOS='veiculos'
)


class OlxApi(object):

    def __init__(self, cidade, categoria):
        self.cidade = cidade
        self.categoria = categoria
        self.response = ()

    @property
    def url(self):
        return 'http://{0}.olx.com.br/{1}'.format(self.cidade, self.categoria)

    @query_string
    def find(self, q=None):
        """
            Método realiza busca das informações desejadas.
        """
        r = requests.request("GET", q)
        if r.status_code != 200:
            raise OlxException()
        soup = BeautifulSoup(r.content)

        for li in soup.find('div', 'section_OLXad-list').find_all('li', 'item'):
            iten = self._extract(li)
            self.response = self.response + (iten,)
        return self

    def _extract(self, content):
        """
            Método extrai as informações desejadas do elemento html.
        """
        iten = {
            "title": "",
            "published": "",
            "location": "",
            "price": "R$ 0,00",
            "url": "",
        }
        iten['url'] = content.a.get('href')
        iten['title'] = content.find('h3', 'OLXad-list-title')\
            .get_text().strip()
        try:
            iten['price'] = content.find('p', 'OLXad-list-price')\
                .get_text().strip()
        except:
            pass
        return iten

if __name__ == '__main__':
    bom = OlxApi(CITY_OLX.RJ, CATEGORY_OLX.INSTRUMENTOS_MUSICAIS)
    print bom.find(q='yamaha trb').response
