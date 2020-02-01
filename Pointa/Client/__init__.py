import getopt
import json
import time
from os import system
from platform import system
from sys import argv

import requests

from .Game import Client
from .locales import en_US, zh_CN

locales = {
    'zh_CN': zh_CN,
    'en_US': en_US
}

opts,args = getopt.getopt(argv[1:],'-l:',['locale='])
for opt_name,opt_value in opts:
    if opt_name in ('-l', '--locale'):
        locale = locales[opt_value]

URL_STRUCT = '{0}/inGame/{1}?fts={2}&r={3}&p={4}'

localVar = {
    'progress': {
        'round': 0,
        'phase': 0
    },
    'playerStat': {},
    'localLog': [],
    'targetUri': '',
    'key': 'null',
    'username': ''
}
anotherPlayer = {
    'key': '',
    'name': ''
}
clientStatus = {
    'inGame': False,
    'loggedIn': False,
    'waiting': False,
}

varsBundle = [localVar, anotherPlayer, clientStatus]

client = Client(system(), locale, varsBundle, URL_STRUCT)

Version = 'Pointa! v0.22-alpha [2020/2/1]'

print(Version)

# Game Begin
if client.Login():
    while not client.clientStatus['inGame']:
        client.Menu()
    preprocess = True
else:
    preprocess = False

while preprocess:
    if not client.Game():
        break

quit()
