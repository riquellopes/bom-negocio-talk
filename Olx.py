# coding: utf-8

import requests
from functools import wraps
from bs4 import BeautifulSoup


class OlxException(Exception):
    pass


def query_string(func):
    """
        Antes que o método find seja invocado, o decorador verifica
        se a variavel 'q' possui algum valor definido::
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            q = args[0]
        except IndexError:
            q = kwargs.get('q')

        if q is not None:
            self.query = q.replace(' ', '+').strip()
            url = "%s?q=%s" % (self.url, self.query)
        else:
            raise OlxException("Nenhum valor foi passado para o Olx.")
        return func(self, q=url)
    return wrapper


class OlxList(list):

    def __init__(self, **kwargs):
        for k in kwargs:
            self.append({k.upper(): kwargs[k]})

    def __getattr__(self, name):
        for l in self:
            try:
                return l[name.upper()]
            except KeyError:
                continue
        raise IndexError("")

CITY_OLX = OlxList(
    RJ='rj',
    SP='sp',
    RR='rr',
    AM='am',
    AC='ac',
    RO='ro',
    MT='mt',
    GO='go',
    TO='to',
    BA='ba',
    ES='es',
    SE='se',
    AL='al',
    RN='rn',
    PB='pb',
    MA='ma',
    PR='pr',
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

    @property
    def url(self):
        return 'http://{0}.olx.com.br/{1}'.format(self.cidade, self.categoria)

    @query_string
    def find(self, q=None):
        """
            Método realiza busca das informações desejadas::
        """
        self.response = ()
        response = self.response
        r = requests.request("GET", q)
        soup = BeautifulSoup(r.content)

        for li in soup.find('div', 'section_OLXad-list').find_all('li', 'item'):
            try:
                price = li.find('p', 'OLXad-list-price').get_text().strip()
            except:
                price = 'R$ 0,00'
            iten = {'title': li.find('h3', 'OLXad-list-title').get_text().strip(),
                    'thumb': "",
                    'published': "",
                    'location': "",
                    'price': price,
                    'url': li.a.get('href')}
            response = response + (iten,)
            self.response = response
        return self

    def _extract_one(self, content):
        """
            Método extra as informações desejadas do elemento html.
        """
        iten = {
            "title": "",
            "published": "",
            "location": "",
            "price": "",
            "url": "",
        }
        extract_itens['price'] = 'R$ 0,00'
        extract_itens['url'] = content.a.get('href')
        extract_itens['title'] = content.find('h3', 'OLXad-list-title')\
            .get_text().strip()
        try:
            extract_itens['price'] = content.find('p', 'OLXad-list-price')\
                .get_text().strip()
        except:
            pass
        return iten.update(extract_itens or {})

    def get_response(self):
        return self.response

    def sort(self, alg=None):
        reverse = alg == 'price_max'

        def getKey(item):
            return item['price']
        self.response = sorted(self.response, key=getKey, reverse=reverse)
        return self

if __name__ == '__main__':
    bom = OlxApi(CITY_OLX.RJ, CATEGORY_OLX.INSTRUMENTOS_MUSICAIS)
    print bom.find(q='yamaha trb').response
