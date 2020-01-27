import asyncio
import json
import math
import random
import threading
import time
from os import path

from flask import Blueprint, Flask, g, jsonify, session
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

import Authorization
from .configs.Config import UserConfig
from DynamicEventLoop import DynamicEventLoop
from Pointa import Player, Pointa
from webapp import PointaMain

Blueprints = {
    '/pointa/': PointaMain
}


def create_app(config, bps: dict):
    app = Flask(__name__)
    for ep, bp in bps.items():
        app.register_blueprint(bp, url_prefix=ep)

    # Event Loop
    loop = asyncio.get_event_loop()
    Del = DynamicEventLoop(loop)
    Del.run()

    @app.before_first_request
    def init():
        with app.app_context():
            g.keyPair = Authorization.load()
            g.playerList = {}
            g.matchList = {}
            g.tLopp = Del

    return app


def Serve(port: int):
    httpServer = HTTPServer(WSGIContainer(create_app(UserConfig, Blueprints)))
    httpServer.listen(5000)
    IOLoop.instance().start()
