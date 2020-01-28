import asyncio
import uuid

from flask import Flask, g, jsonify, request, session, abort

from . import Authorization
from .Pointa import Player, Pointa

from .DynamicEventLoop import DynamicEventLoop

data = None

app = Flask(__name__)

class Data:
    def __init__(self):
        self.playerList = {}
        self.matchList = {}

data = Data()
Del = DynamicEventLoop()
Del.run()

# Handling Requests Outside the Game period
@app.route('/outGame/<key>', methods=['POST'])
def outGameHandler(key):
    global data
    global Del
    req = request.get_json(force=True)
    Data = data
    Loop = Del

    if req['Action'] == 'Ready':
        # Generate a uid as key
        Data.playerList.update({key: Player(key)})
        uid = uuid.uuid5(uuid.NAMESPACE_DNS, request.remote_addr)
        return jsonify({'UUID': str(uid)})

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
        else:
            abort(404)

@app.route('/inGame/<key>', methods=['GET', 'POST'])
def inGameHandler(key):
    global data
    global Del
    req = request.get_json(force=True)
    Data = data

    currentMatch = None

    # Find current match
    for match in Data.matchList.items():
            if key in match[0]:
                currentMatch = match[1]
                another = [x for x in match[0] if x!=key][0]
                break

    if currentMatch == None:
        abort(404)

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
        abort(405)
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
                    'self': [
                        stat['players'][key].properties,
                        stat['players'][key].actions
                    ],
                    'another': [
                        stat['players'][another].properties,
                        stat['players'][another].actions,
                        stat['players'][another].key
                    ]
                }
            }
        )
