import json
import selectors
import socket

import Authorization


class Pointa_Client():

    def __init__(self, target_uri, socket_object=None):

        # Setting up
        self.target = tuple(target_uri.split(':'))
        self.selector = selectors.DefaultSelector()

        # Set Keypair
        if Authorization.checkNew():
            self.keys = Authorization.newUser()
        else:
            self.keys = Authorization.getKeys()

        # Set Socket
        if socket_object:
            self.sock = socket
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.connect(self.target)
        self.sock.setblocking(False)

        self.selector.register(
            self.sock,
            selectors.EVENT_READ | selectors.EVENT_WRITE,
        )

        self.messageArray = []
        self.loopVars = {}

    def insertMessage(self, verb, detail, nround=-1):
        self.messageArray.append(json.dump(
            {
                'From': self.keys[0],
                'Command': verb,
                'Detail': detail,
                'Round': nround
            }
        ))

    def eventHandler(self):
        for key, mask in self.selector.select(timeout=1):
            self.loopVars['connection'] = key.fileobj

            if mask & selectors.EVENT_READ:
                return json.loads(self.loopVars['connection'].recv(1024))

            if mask & selectors.EVENT_WRITE:
                self.loopVars['message'] = self.messageArray.pop(0)
                self.loopVars['connection'].sendall(self.loopVars['message'])
                return self.loopVars['currentMessage']
