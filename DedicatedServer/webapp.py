from flask import Flask, g, session, Blueprint, jsonify, request

PointaMain = Blueprint('PointaMain', __name__)


@PointaMain.route('/outGame/<key>', methods=['POST'])
def outGameHandler(key):
    data = request.json
    if data['Action'] == 'Ready':
        g.playerList
