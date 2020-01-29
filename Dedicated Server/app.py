import asyncio
import time
import uuid

from flask import Flask, abort, g, jsonify, request, session

from .DynamicEventLoop import DynamicEventLoop
from .Pointa import Player, Pointa

data = None

app = Flask(__name__)

class Data:
    def __init__(self):
        self.playerList = {}
        self.matchList = {}
        self.req = 0

data = Data()
Del = DynamicEventLoop()
Del.run()

# Lag Remover
@app.before_request
def before():
    global data
    global Del
    data.req += 1
    if data.req % 100 == 0:
        for key, p in data.playerList.items():  # Overtime Detection
            if int(time.time()) - p[1] >= 60:
                data.playerList.pop(key)
        for key, g in Del.taskList:  # Done match Detection
            if g.done():
                Del.pop(key)

# Handling Requests Outside the Game period
@app.route('/outGame/<key>', methods=['POST'])
def outGameHandler(key):
    global data
    global Del
    req = request.get_json(force=True)

    if req['Action'] == 'Ready':
        # Generate a uid as key
        uid = uuid.uuid5(uuid.NAMESPACE_DNS, request.remote_addr)
        data.playerList.update({uid: (
            Player(uid),
            int(time.time()),  # Last Communicate time
        )})
        return jsonify({'UUID': str(uid)})

    elif req['Action'] == 'Invite':

        data.playerList[key][1] = int(time.time())

        if req['Target'] in g.playerList.keys():

            match = Pointa(
                    data.playerList[key][0],
                    data.playerList[req['Target']][0]
                )

            Del.append(match, match.main())

            data.matchList.update({
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

    data.playerList[key][1] = int(time.time())

    currentMatch = None

    # Find current match
    for match in data.matchList.items():
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
            Data.playerList[key][0].action({
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
        Data.playerList[key][0].localVar = {
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
