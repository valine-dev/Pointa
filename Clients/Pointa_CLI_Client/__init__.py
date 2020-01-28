import json
import time
from os import system

import requests

from . import Authorization

keyPair = Authorization.load()[0]


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
ingameStruct = '/inGame/%a/?finalTimeStamp=%b&round=%c&phase=%d'

def Write():
    actions = input('Actions ("atk,def,hel")> ').split(',')
    purl = f"{targetUri}/inGame/{clientStatus['key']}"
    payload = {
        'Action': [
            actions[0],
            actions[1],
            actions[2]
        ]
    }
    req = requests.post(purl, json=payload)
    if req.status_code != req.ok:
        print('Request failed! Code is ', req.status_code)


# Handling Updated Log Pharse
def Phrase(json):
    for cmd in json['UpdatedLog']:
        if cmd['action'] == 'roundBegin':
            print('\n')
            localVar['Round'] = cmd['value']

        if cmd['action'] == 'pointRolled':
            print(f"{cmd['actor']} Rolled {cmd['value']} Pts!")

        if cmd['action'] == 'phaseBegin':
            if cmd['value']['phase'] == '2':
                # Print players' status
                for tag, p in json['playerStats']:
                    print(
                        f'{tag} | {p[0]}'
                    )
                Write()
            elif cmd['value']['phase'] == '3':
                # Print players' actions
                for tag, p in json['playerStats']:
                    print(
                        f'{tag} | {p[1]}'
                    )
                print('Round ', str(cmd['value']), ' Settled!')
            localVar['phase'] = cmd['value']['phase']

        if cmd['action'] == 'atkJudge':
            print(
                f"{cmd['actor']} Rolled {cmd['value']} for atk judge!"
                )
        localLog.append(cmd)

def Game():
    time.sleep(0.01)
    if localLog == []:
        url = targetUri + (ingameStruct % (
                clientStatus['key'],
                '0',
                '0',
                '0'
            ))
    else:
        url = targetUri + (ingameStruct % (
                clientStatus['key'],
                localLog[-1]['time'],
                localVar['round'],
                localVar['phase']
            ))

    req = requests.get(url)
    if req.status_code == req.ok:
        Phrase(req.json())
    else:
        print('Request failed! Code is ', req.status_code)



# Main Game Loop
while True:
    if clientStatus['inGame']:
        if clientStatus['waiting']:
            url = targetUri + (ingameStruct % (
                clientStatus['key'],
                'none',
                'none',
                'none'
            ))
            req = requests.get(url)
            if req.status_code == req.ok:
                clientStatus['waiting'] = False
                print('Recieved! Game is about to begin!')
                time.sleep(5)
                system('cls')
        else:
            Game()
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
            if req.status_code == req.ok:
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
                'Action': 'Ready',
                'Target': targetKey
            }
            req = requests.post(
                targetUri+'/outGame/'+clientStatus['key'],
                json=payload
            )
            if req.status_code == req.ok:
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
