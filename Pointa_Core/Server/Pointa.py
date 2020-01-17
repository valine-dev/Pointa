import random


class Player:
    'Base Player Class'
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

    def action(self, data):
        self.actions = data

    def roundClear(self):
        self.properties['def'] = 0
        self.actions = {
            0: 0,
            1: 0,
            2: 0
        }

    def roll(self):
        self.properties['pt'] += random.randint(1, 12)


class Pointa:
    'Base Game Emulator, Contains all Game Logics'
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

    def settleRound(self):
        # Step 0, Check if actions are avaliable
        for p in self.players.items():
            if sum(p.actions.items()) > p.properties['pt']:
                return p

        # Setp 1, Sort out the actions.
        for key, p in self.players:
            for action, value in p.actions:
                self.actions.append({
                    'own': key,
                    'action': action,
                    'value': value
                })
        self.actions.sort(key=lambda x: (x['value'], -x['action']))

        # Step 2, Take actions.
        for action in self.actions:
            self.players[action['own']].properties['pt'] -= action['value']

            if action['action'] == 0:  # Attack
                self.temp['target'] = sorted(
                    self.players.pop(action['own']).items())[0]
                self.temp['damage'] = (0.3 * action['value'] ^ 2)
                self.temp['target'].properties['def'] = [
                    0,
                    self.temp['target'].properties['def'] - self.temp['damage']
                ][
                    (self.temp['target'].properties['def'] - self.temp['damage']) > 0
                ]
                self.temp['damage'] -= self.temp['target'].properties['def']
                self.temp['target'].properties['def'] -= self.temp['damage']

            elif action['action'] == 1:
                self.players[action['own']].properties['def'] = (0.25 * action['value'] ^ 2)

            elif action['action'] == 2:
                self.players[action['own']].properties['hp'] = (0.35 * action['value'] ^ 2)
                if self.players[action['own']].properties['hp'] > 100:
                    self.players[action['own']].properties['hp'] = 100
