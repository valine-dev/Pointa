import json
import time
from os import system

import requests


# Setting up local vars
localVar = {
    'round': 0,
    'phase': 0
}
localLog = []
playerStat = {}

clientStatus = {
    'inGame': False,
    'loggedIn': False,
    'waiting': False,
    'key': ''
}

targetUri = ''
ingameStruct = '/inGame/{0}?fts={1}&r={2}&p={3}'

def Write(key):
    actions = input('Actions ("atk,def,hel")> ').split(',')
    print('\n')
    purl = "{0}/inGame/{1}".format(targetUri, key)
    payload = {
        'Action': [
            actions[0],
            actions[1],
            actions[2]
        ]
    }
    req = requests.post(purl, json=payload)
    if req.status_code == 405:
        print('OverTimed or Bad Input!')

def Phrase(json, localVar, localLog, key):
    for cmd in json['UpdatedLog']:
        if cmd['action'] == 'roundBegin':
            print('\n')
            print(f"--------Round-{cmd['value']}---------")
            localVar['round'] = cmd['value']

        elif cmd['action'] == 'pointRolled':
            print(f"{cmd['actor']} Rolled {cmd['value']} Pts!")

        elif cmd['action'] == 'phaseBegin':
            if cmd['value']['phase'] == 2:
                print('Now, Player status are...')
                for tag, p in json['playerStats'].items():
                    print(
                        f'{tag} | {p[0]}'
                    )
                Write(key)
            elif cmd['value']['phase'] == 3:
                print('\nNow, Player Actions are...')
                for tag, p in json['playerStats'].items():
                    print(
                        f'{tag} | {p[1]}'
                    )
                print('Round ', str(cmd['value']), ' Settled!')
            localVar['phase'] = cmd['value']['phase']

        elif cmd['action'] == 'atkJudge':
            print(
                f"{cmd['actor']} Rolled {cmd['value']} for atk judge!"
                )

        elif cmd['action'] == 'playerKilled':
            print('Player', str(cmd['value']), 'was Killed!')

        elif cmd['action'] == 'gameEnd':
            print('Game over.', )
            print('Now, Player status are...')
            for tag, p in json['playerStats'].items():
                    print(
                        f'{tag} | {p[1]}'
                    )
            return True
        localLog.append(cmd)
        return False

def Game():
    time.sleep(0.01)
    if localLog == []:
        url = targetUri + ingameStruct.format(
                clientStatus['key'],
                '0',
                '0',
                '0'
            )
    else:
        url = targetUri + ingameStruct.format(
                clientStatus['key'],
                localLog[-1]['time'],
                localVar['round'],
                localVar['phase']
            )

    req = requests.get(url)
    if req.status_code == 200:
        if Phrase(req.json(), localVar, localLog, clientStatus['key']):
            return True
    else:
        print('Request failed! Code is ', req.status_code)
    return False



# Main Game Loop
while True:
    if clientStatus['inGame']:
        if clientStatus['waiting']:
            url = targetUri + ingameStruct.format(
                clientStatus['key'],
                '0',
                '0',
                '0'
            )
            req = requests.get(url)
            if req.status_code == 200:
                clientStatus['waiting'] = False
                print('Recieved! Game is about to begin!')
                time.sleep(5)
                system('cls')
        else:
            if Game():
                break
    else:
        # Out Game Process
        if not clientStatus['loggedIn']:
            # Join Process
            payload = {'Action': 'Ready'}
            targetUri = input("Input Target Server's Uri > ")
            # Send Login Request
            req = requests.post(
                targetUri+'/outGame/'+'null',
                json=payload
            )
            if req.status_code == 200:
                clientStatus['key'] = req.json()['UUID']
                print('Logged in! Your key is ', clientStatus['key'])
                clientStatus['loggedIn'] = True
            else:
                print('Logged failed! Code is ', req.status_code)

        # Identity adjust
        identity = input('Your Identity (Inviter/Reciever) > ')
        if identity == 'Inviter':
            targetKey = input('You want to invite (Key)... > ')

            # Generate Request
            payload = {
                'Action': 'Invite',
                'Target': targetKey
            }
            req = requests.post(
                targetUri+'/outGame/'+clientStatus['key'],
                json=payload
            )
            if req.status_code == 200:
                print('Invited! Game is about to begin!')
                clientStatus['inGame'] = True
                time.sleep(5)
                system('cls')
            elif req.status_code == 404:
                print('Player not found!')
            else:
                print('Request failed! Code is ', req.status_code)

        elif identity == 'Reciever':
            clientStatus['inGame'] = True
            clientStatus['waiting'] = True
        else:
            print('Bad input!')
