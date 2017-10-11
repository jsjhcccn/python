import os
import random
from entity.proxyentity import ProxyEntity


class proxyreader():
    def __init__(self):
        self.__lista = []
        self.__proxinfo =  {'host': "",'port': 0, 'user': "",'pass': ""}
        if os.access(os.path.dirname(os.path.abspath(__file__)).replace("toolunit", "proxyconfig\\proxy.prop"), os.R_OK):
            for line in open(os.path.dirname(os.path.abspath(__file__)).replace("toolunit", "proxyconfig\\proxy.prop")):
                serverlst = line.split(',')
                if len(serverlst) > 0:
                    serveritem = ProxyEntity(
                        serverlst[0], serverlst[1], serverlst[2], serverlst[3])
                    self.__lista.append(serveritem)
   

    def getProxyClientConfig(self):
        if len(self.__lista) > 0:
            proxyitem = self.__lista[random.randint(0, len(self.__lista))]
            if proxyitem is not None:
                __proxinfo = {
                    'host': proxyitem.ip,
                    'port': int(proxyitem.port),
                    'user': proxyitem.username,
                    'pass': proxyitem.userpassword
                }
        return __proxinfo
