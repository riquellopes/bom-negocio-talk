# coding: utf-8
import urllib
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
            raise OlxException("Nenhum valor foi passado para o BomNegócio.")
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
        response = ()
        soup = BeautifulSoup(urllib.urlopen(q).read())
        for li in soup.find_all('li', 'list_adsBN_item'):
            print 'AAA'
            try:
                price = li.find('p', 'price').get_text().strip()
            except:
                price = '0,00'
            iten = {'title': li.h3.a.get_text(),
                    'price': price,
                    "url": li.a['href']}
            response = response + (iten,)
            self.response = response
        return self

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
    print bom.find(q='yamaha trb').get_response()
