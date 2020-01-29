import getopt
import json
import math
import random
import threading
import time
from os import path
from sys import argv

from flask import Blueprint, Flask, g, jsonify, session
from gevent.pywsgi import WSGIServer

from .app import Data, app
from .configs.Config import UserConfig
from .DynamicEventLoop import DynamicEventLoop
from .Pointa import Player, Pointa


def init_app(config):
    # Init the app
    app.config.from_object(UserConfig)
    return app


def Serve(port: int):
    httpServer = WSGIServer(('0.0.0.0', port), init_app(UserConfig))
    print('Production Env Server ON.')
    httpServer.serve_forever()
