import asyncio

from flask import Flask, g, jsonify, request, session

from . import Authorization
from .Pointa import Player, Pointa

from .DynamicEventLoop import DynamicEventLoop

app = Flask(__name__)

class Data:
    def __init__(self):
        self.playerList = {}
        self.matchList = {}


@app.before_first_request
def init():
    with app.app_context():
        g._keyPair = Authorization.load()
        g._data = Data()
        # Looper
        loop = asyncio.get_event_loop()
        Del = DynamicEventLoop(loop)
        Del.run()
        g._DLoop = Del

# Handling Requests Outside the Game period
@app.route('/outGame/<key>', methods=['POST'])
def outGameHandler(key):
    req = request.json
    Data = getattr(g, '_data', None)
    Loop = getattr(g, '_DLoop', None)

    if req['Action'] == 'Ready':
        Data.playerList.update({key: Player(key)})
        return jsonify({'Action': 'Accepted'})

    elif req['Action'] == 'Invite':

        if req['Target'] in g.playerList.keys():

            match = Pointa(
                    Data.playerList[key],
                    Data.playerList[req['Target']]
                )

            Loop.append(match, match.main())

            Data.matchList.update({
                (key, req['Target']): match
            })

        return jsonify({'Action': 'Accepted'})

@app.route('/inGame/<key>', methods=['GET', 'POST'])
def inGameHandler(key):
    req = request.json
    Data = getattr(g, '_data', None)

    # Find current match
    for match in Data.matchList.items():
            if key in match[0]:
                currentMatch = match[1]
                another = [x for x in match[0] if x!=key][0]
                break

    # Insert Action
    if request.method == 'POST':
        if currentMatch.round['phase'] == 2:
            dat = req['Action']
            Data.playerList[key].action({
                0: dat[0],
                1: dat[1],
                2: dat[2]
            })
            return jsonify({'Action': 'Accepted'})
        return jsonify({'Action': 'Denied'})
    elif request.method == 'GET':
        # Get request args
        fTS = int(request.args.get("finalTimeStamp"))
        roundL = int(request.args.get("round"))
        phaseL = int(request.args.get("phase"))

        # Sync Local Vars to Player Object
        Data.playerList[key].localVar = {
            'round': roundL,
            'phase': phaseL
        }

        # Get Updated Log
        stat = currentMatch.getStat()
        uptLog = list(
            filter(
                lambda x: x['time'] > fTS,
                stat['log']
            )
        )
        # Return Sync Result in Standard Format
        return jsonify(
            {
                'UpdatedLog': uptLog,
                'playerStats': {
                    key: [
                        stat['players'][key].properties,
                        stat['players'][key].actions
                    ],
                    another: [
                        stat['players'][another].properties,
                        stat['players'][another].actions
                    ]
                }
            }
        )
