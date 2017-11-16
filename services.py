#!/usr/bin/env python3

from canvas import canvasAccessToken 
import pymongo
from pymongo import MongoClient
from flask import Flask
import requests
from flask.ext.discoverer import Discoverer, advertise

clientIP = "127.0.0.1"
clientPORT = 27017
client = MongoClient(clientIP, clientPORT)
canvas = client.canvas
auth = client.auth

app = Flask(__name__)
#disco = Discoverer(app)


@advertise(private=True, colors=[])
@app.route('/route1', methods=['GET'])
def route1():
    print('Route 1 accessed')
    # do something
    return "route1"


@advertise(private=True, colors=[])
@app.route('/route2', methods=['GET'])
def route2():
    print('Route 2 accessed')
    # do something
    return "route2"


@advertise(private=True, colors=[])
@app.route('/route3', methods=['POST'])
def route3():
    print('Route 3 accessed')
    # do something
    return "route3"


@advertise(private=True, colors=[])
@app.route('/route4', methods=['POST'])
def route4():
    print('Route 4 accessed')
    # do something
    return "route4"


app.run(host='0.0.0.0', debug=True)
