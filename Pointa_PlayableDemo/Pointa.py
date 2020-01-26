import asyncio
import random
import math
import time


class Player(object):
    '''
    Player Class
    '''
    def __init__(self, key):
        self.key = key
        self.properties = {
            'hp': 100,
            'pt': 0,
            'def': 0
        }
        # 0 = atk, 1 = def, 2 = hel
        self.actions = {
            0: 0,
            1: 0,
            2: 0
        }

        self.temp = {}

    def action(self, data):
        if sum(data.values()) > self.properties['pt']:
            return 'Illegal input!'
        self.properties['pt'] -= sum(data.values())
        self.actions = data

    def roundClear(self):
        self.properties['def'] = 0
        self.actions = {
            0: 0,
            1: 0,
            2: 0
        }

    def roll(self):
        self.temp['roll'] = random.randint(1, 12)
        self.properties['pt'] += self.temp['roll']
        return self.temp['roll']

    def damage(self, pt):
        'Interface Calculates the damage'

        # Set a random judge number affacts actual damage
        self.temp['judge'] = random.randint(1, 12)

        # Calculate the actual damage by the judge number and used pt
        if self.temp['judge'] in range(1, 6):
            self.temp['dmg'] = math.ceil((0.30 * pow(pt, 2)) * 0.5)
        elif self.temp['judge'] in range(6, 12):
            self.temp['dmg'] = math.ceil(0.30 * pow(pt, 2))
        elif self.temp['judge'] == 12:
            self.temp['dmg'] = math.ceil((0.30 * pow(pt, 2)) * 1.5)

        # Temporary stores the defense value
        self.temp['def'] = self.properties['def']

        # Calculate the final defense value
        self.properties['def'] = [
            0,
            self.properties['def'] - self.temp['dmg']
        ][
            self.properties['def'] > self.temp['dmg']
        ]

        # Calculate the final damage to the player
        self.temp['dmg'] = [
            0,
            self.temp['dmg'] - self.temp['def']
        ][
            self.temp['dmg'] > self.temp['def']
        ]

        # Calculate the player's hp
        self.properties['hp'] -= self.temp['dmg']

        # Return the judge number ready to be caught by logger
        return self.temp['judge']


class Pointa(object):
    '''
    Game Logics
    '''
    def __init__(self, p1, p2):
        self.players = {
            p1.key: p1,
            p2.key: p2
        }
        self.round = {
            'num': 0,
            'phase': 0
        }
        self.actions = []
        self.temp = {}
        self.log = []

        self.status = {}

    def settleRound(self):
        # Setp 1, Sort out the actions.
        for key, p in self.players.items():
            for action, value in p.actions.items():
                self.actions.append({
                    'own': key,
                    'action': action,
                    'value': value
                })
        self.actions.sort(key=lambda x: (x['value'], -x['action']))

        # Step 2, Take actions.
        for action in self.actions:
            # Ignore null action
            if action['value'] != 0:
                if action['action'] == 0:  # Attack
                    self.temp['target'] = list(filter(
                        lambda x: x[0] != action['own'],
                        self.players.items()
                    ))[0][1]
                    self.logger(
                        action['own'],
                        'atkJudge',
                        self.temp['target'].damage(action['value'])
                        )

                elif action['action'] == 1:  # Defense
                    self.players[
                        action['own']
                    ].properties[
                        'def'
                    ] = (0.25 * pow(action['value'], 2))

                elif action['action'] == 2:  # Healing
                    self.players[
                        action['own']
                    ].properties[
                        'hp'
                    ] += (0.35 * pow(action['value'], 2))

                    # Make sure the healing action won't break the max health
                    if self.players[action['own']].properties['hp'] > 100:
                        self.players[action['own']].properties['hp'] = 100

        # Step 3, Clear the actions and wait for next Cauculating
        for key, p in self.players.items():
            p.roundClear()

    def logger(self, actor, action, value):
        self.log.append(
            {
                'time': time.time(),
                'actor': actor,
                'action': action,
                'value': value
            }
        )

    def getLog(self):
        return self.log

    async def main(self):
        'Main game Emulator'
        self.round['num'] += 1
        self.logger('game', 'roundBegin', self.round['num'])

        # Phase 1 - Roll the points
        self.round['phase'] = 1
        self.logger('game', 'phaseBegin', self.round)
        for key, p in self.players.items():
            self.logger(key, 'pointRolled', p.roll())

        # Phase 2 - Wait for the actions
        self.round['phase'] = 2
        self.logger('game', 'phaseBegin', self.round)
        await asyncio.sleep(15)

        # Phase 3 - Calculate the actions
        self.round['phase'] = 3
        self.logger('game', 'phaseBegin', self.round)
        self.settleRound()

        # Return the failure
        for key, p in self.players.items():
            if p.properties['hp'] < 1:
                return p

        # Next Round
        await self.main()
