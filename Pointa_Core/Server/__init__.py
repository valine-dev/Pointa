import json
import logging
from socketserver import StreamRequestHandler

import Authorization

from .Pointa import Player, Pointa


class Handler(StreamRequestHandler):
    playerList = {}
    matchList = {}

    keys = Authorization.load()

    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.INFO)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.INFO)
    consoleHandler.setFormatter(
        logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'
        )
    )

    fileHandler = logging.FileHandler('server.log')
    fileHandler.setLevel(logging.INFO)
    fileHandler.setFormatter(
        logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'
        )
    )

    _logger.addHandler(consoleHandler)
    _logger.addHandler(fileHandler)

    def handle(self):
        Handler._logger.info('%i Connected' % self.client_address[0])
        self.msg = json.loads(self.rfile.read())

        # Handle Connect Command
        if self.msg['Command'] == 'Connect':
            Handler.playerList.update({
                self.msg['Detail']: {
                    'IP': self.client_address[0],
                    'Player': Player(self.msg['Detail'])
                }
            })
        
        # Handle Match Command
        elif self.msg['Command'] == 'Match':
            if self.msg['detail']

