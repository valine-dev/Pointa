import asyncio
import time
import uuid
import random

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
        self.taskList = {}

data = Data()
Del = DynamicEventLoop()
Del.run()

# Lag Remover
@app.before_request
def before():
    global data
    global Del
    data.req += 1
    if data.req % 1000 == 0:
        temps = [
            list(data.playerList.items()),
            list(Del.taskList.items())
        ]
        for key, p in temps[0]:  # Overtime Detection
            if int(time.time()) - p[1] >= 60:
                data.playerList.pop(key)
        for key, ga in temps[1]:  # Done match Detection
            if ga.done():
                Del.pop(key)

# Handling Requests Outside the Game period
@app.route('/outGame/<key>', methods=['POST'])
def outGameHandler(key):
    global data
    global Del
    req = request.get_json(force=True)

    if req['Action'] == 'Ready':
        # Generate a uid as key
        uid = uuid.uuid5(uuid.NAMESPACE_DNS, request.remote_addr + str(random.randint(0, 100)))
        data.playerList.update({str(uid): [
            Player(str(uid)),
            int(time.time()),  # Last Communicate time
        ]})
        return jsonify({'UUID': str(uid)})

    elif req['Action'] == 'Invite':

        data.playerList[key][1] = int(time.time())

        if req['Target'] in data.playerList.keys():

            match = Pointa(
                    data.playerList[key][0],
                    data.playerList[req['Target']][0],
                    Del.loop
                )
            Del.append(match, match.main())

            keys = (key + ',' + req['Target'])
            data.matchList.update({
                keys: match
            })

            return jsonify({'Action': 'Accepted'})
        else:
            abort(404)

# Handling Requests in the Game period
@app.route('/inGame/<key>', methods=['GET', 'POST'])
def inGameHandler(key):
    global data
    global Del
    Data = data

    # Updating last communicating time 
    data.playerList[key][1] = int(time.time())

    currentMatches = []

    # Find current match
    for match in data.matchList.items():
            if key in match[0].split(','):
                currentMatches.append(match[1])
                another = [x for x in match[0].split(',') if x!=key][0]
                break

    try:
        currentMatch = currentMatches[0]
    except IndexError:
        abort(404)

    # Insert Action
    if request.method == 'POST':
        req = request.get_json(force=True)
        if currentMatch.round['phase'] == 2:
            dat = req['Action']
            Data.playerList[key][0].action({
                0: int(dat[0]),
                1: int(dat[1]),
                2: int(dat[2])
            })
            return jsonify({'Action': 'Accepted'})
        abort(405)

    elif request.method == 'GET':
        # Get request args
        fTS = int(request.args.get("fts"))
        roundL = int(request.args.get("r"))
        phaseL = int(request.args.get("p"))
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

        anotherAction = {}
        # Avoid Client Cheating
        if currentMatch.round['phase'] == 3:
            anotherAction = stat['players'][another].actions

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
                        anotherAction,
                        stat['players'][another].key
                    ]
                }
            }
        )
