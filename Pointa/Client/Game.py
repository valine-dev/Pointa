import json
import time
from os import system

import requests


class Client:
    '''Client Class
    '''

    def __init__(self, os: str, lang: object, varsBundle: list, struct: str):
        # Clean Command
        if os == 'Windows':
            self.clear = 'cls'
        elif os == 'Linux' or 'Darwin':
            self.clear = 'clear'

        self.URL_STRUCT = struct

        self.lang = lang

        self.atkJudgeCache = {}
        self.deadCache = []

        # Loading Vars
        self.localVar = varsBundle[0]
        self.anotherPlayer = varsBundle[1]
        self.clientStatus = varsBundle[2]

    def ARinput(self, sign: str, exitable=True):
        try:
            return input(sign)
        except KeyboardInterrupt:
            if exitable:
                if self.clientStatus['loggedIn']:
                    # Send quit request to server
                    url = f"{self.localVar['targetUri']}/outGame/{self.localVar['key']}"
                    payload = {
                        'Action': 'Quit'
                    }
                    requests.post(url, json=payload)
                quit()
            else:
                pass

    def Login(self):
        '''Login Process, returns true if Success
        '''
        # Get Input
        self.localVar['targetUri'] = self.ARinput(self.lang.LOGIN_SERVER)
        self.localVar['username'] = self.ARinput(self.lang.LOGIN_USERNAME)

        # Make request
        payload = {
            'Action': 'Ready',
            'Target': self.localVar['username']
        }
        url = f"{self.localVar['targetUri']}/outGame/{self.localVar['key']}"
        try:
            req = requests.post(url, json=payload)
        except ConnectionRefusedError:
            print(self.lang.BAD_INPUT)
            return False

        # Get Result
        if req.status_code == 200:
            self.localVar['key'] = req.json()['UUID']
            self.clientStatus['loggedIn'] = True
            return True
        else:
            print(self.lang.REQUEST_ERROR.format(code=str(req.status_code)))
            return False

    def Menu(self):
        '''Menu Stage, Call after Login(), before Game Loop
        '''
        system(self.clear)  # Clear Screen
        print(self.lang.MENU.format(key=self.localVar['key']))
        choose = self.ARinput(self.lang.MENU_SELECT)
        if choose == '0':
            p = self.ARinput(self.lang.INVITE)

            # Make Request
            payload = {
                'Action': 'Invite',
                'Target': p
            }
            url = f"{self.localVar['targetUri']}/outGame/{self.localVar['key']}"
            req = requests.post(url, json=payload)

            # Result
            if req.status_code == 200:
                self.anotherPlayer['key'] = p
                self.anotherPlayer['name'] = req.json()['targetName']
                print(self.lang.GAME_START.format(name=self.anotherPlayer['name']))
                self.clientStatus['inGame'] = True
                time.sleep(5)  
                system(self.clear)  # Clear Screen
                return True
            elif req.status_code == 404:
                print(self.lang.INVITE_404)
            else:
                print(self.lang.REQUEST_ERROR.format(code=req.status_code))

        elif choose == '1':
            print(self.lang.WAIT)
            url = self.URL_STRUCT.format(
                    self.localVar['targetUri'],
                    self.localVar['key'],
                    '0',
                    '0',
                    '0'
                )
            # Waiting Loop
            while requests.get(url).status_code != 200:
                pass
            json = requests.get(url).json()
            ar = json['playerStats']['another']
            self.anotherPlayer['key'] = ar[2]
            self.anotherPlayer['name'] = ar[3]
            print(self.lang.GAME_START.format(name=self.anotherPlayer['name']))
            # Ready to Game
            self.clientStatus['inGame'] = True
            time.sleep(5)  
            system(self.clear)  # Clear Screen
            return True

        elif choose == '2':
            quit()

        else:
            print(self.lang.BAD_INPUT)
            time.sleep(5)
            return False

    def Write(self):
        '''Tool Method, Waiting Player's Action
        '''
        actions = []
        for action in ['ATK', 'DEF', 'HEL']:
            while True:
                try:
                    actions.append(
                        int(self.ARinput(self.lang.ACTION.format(ACTION=action)))
                    )
                except ValueError:  # Bad Input...
                    print(self.lang.BAD_INPUT)
                else:
                    break
        purl = "{0}/inGame/{1}".format(
            self.localVar['targetUri'],
            self.localVar['key']
        )
        payload = {
            'Action': [
                actions[0],
                actions[1],
                actions[2]
            ]
        }
        print(self.lang.WAIT)
        req = requests.post(purl, json=payload)
        if req.status_code == 405:
            print(self.lang.TIMEOUT_BAD)

    def Phraser(self, json):
        '''Tool Method, Phrase Updated log
        When returns True, game should be continue.
        '''
        nameMap = {
            'self': self.localVar['username'],
            'another': self.anotherPlayer['name']
            }
        callMap = {
            self.localVar['key']: 'self',
            self.anotherPlayer['key']: 'another'
        }
        for cmd in json['UpdatedLog']:
            if cmd['action'] == 'roundBegin':
                self.atkJudgeCache = {}
                self.localVar['progress']['round'] = cmd['value']
                # Give Output
                print(self.lang.ROUND_BEGIN.format(num=cmd['value']))

            elif cmd['action'] == 'pointRolled':
                print(self.lang.ROLLED.format(name=nameMap[callMap[cmd['actor']]], num=cmd['value']))

            elif cmd['action'] == 'phaseBegin':
                if cmd['value']['phase'] == 2:
                    for tag, p in json['playerStats'].items():
                        print(self.lang.STATUS.format(
                            name=nameMap[tag],
                            HP=p[0]['hp'],
                            DEF=p[0]['def'],
                            PT=p[0]['pt']
                        ))
                    print(self.lang.PHASE_2)
                    self.Write()

                elif cmd['value']['phase'] == 3:
                    # Output table head
                    print(self.lang.ACTIONS_HEAD.format(num=cmd['value']['num']))
                    actions = []
                    # Sorting actions from both players
                    for t, p in json['playerStats'].items():
                        for action in p[1].items():
                            actions.append({
                                'owner': nameMap[t],
                                # Because there are no calculates here...
                                'action': str(action[0]),
                                'value': str(action[1])
                            })
                    actions.sort(key=lambda x: (int(x['value']), -int(x['action'])))
                    # Print them.
                    for action in actions:
                        if action['value'] != '0':
                            if action['action'] == '0':
                                print(self.lang.ACTION_ATK.format(
                                    name=action['owner'],
                                    num=action['value'],
                                    judge=self.atkJudgeCache[action['owner']]
                                ))
                            elif action['action'] == '1':
                                print(self.lang.ACTION_DEF.format(
                                    name=action['owner'],
                                    num=action['value']
                                ))
                            elif action['action'] == '2':
                                print(self.lang.ACTION_HEL.format(
                                    name=action['owner'],
                                    num=action['value']
                                ))
                self.localVar['progress']['phase'] = cmd['value']['phase']

            elif cmd['action'] == 'atkJudge':
                # Temporary cache the atkJudge
                self.atkJudgeCache.update(
                    {
                        nameMap[callMap[cmd['actor']]]: cmd['value']
                    }
                )

            elif cmd['action'] == 'playerKilled':
                print(self.lang.PLAYER_KILLED.format(
                    name=nameMap[callMap[cmd['value']]]
                ))
                self.deadCache.append(nameMap[callMap[cmd['value']]])

            elif cmd['action'] == 'gameEnd':
                # Send quit request to server
                url = f"{self.localVar['targetUri']}/outGame/{self.localVar['key']}"
                payload = {
                    'Action': 'Quit'
                }
                requests.post(url, json=payload)

                print(self.lang.GAME_END.format(
                    lose=self.deadCache[0]
                ))

            self.localVar['localLog'].append(cmd)
        return True

    def Game(self):
        '''When returns True, game should be continue.
        '''
        time.sleep(0.01)
        if self.localVar['localLog'] == []:
            fts = '0'
        else:
            fts = self.localVar['localLog'][-1]['time']
        url = self.URL_STRUCT.format(
            self.localVar['targetUri'],
            self.localVar['key'],
            fts,
            self.localVar['progress']['round'],
            self.localVar['progress']['phase']
        )
        req = requests.get(url)
        if req.status_code == 200:
            return self.Phraser(req.json())
        else:
            print(self.lang.REQUEST_ERROR.format(code=str(req.status_code)))
        return False
