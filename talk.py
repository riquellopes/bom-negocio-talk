# coding: utf-8
from lib.PyGtalkRobot import GtalkRobot
from olx import (
    OlxApi, CITY_OLX, CATEGORY_OLX
)


class OlxBot(GtalkRobot):

    def __init__(self, **kwargs):
        super(OlxBot, self).__init__(**kwargs)
        self.api = OlxApi(CITY_OLX.RJ, CATEGORY_OLX.INSTRUMENTOS_MUSICAIS)

    def command_003_search(self, user, msg, args):
        """(search)( +(.*))?$(?i)"""
        responses = self.api.find(q=args[1]).sort().get_response()[:5]
        message = []
        for r in responses:
            message.append("Titulo: {0} - Preço: {1}\nLink: {2}".format(
                r['title'].encode('utf-8').strip(), r['price'], r['url']))
        message = "\n\n".join(message)
        self.replyMessage(user, message)

if __name__ == "__main__":
    import getpass
    user = raw_input("Digite seu gmail: ")
    pasw = getpass.getpass("Digite sua senha: ")

    bot = OlxBot()
    bot.setState('available', "TestBot")
    bot.start(user, pasw)
