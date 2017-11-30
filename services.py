#!/usr/bin/env python3

import warnings
from flask.exthook import ExtDeprecationWarning
warnings.simplefilter("ignore", ExtDeprecationWarning)

from canvas import canvasAccessToken
import pymongo
from flask import Flask, request, Response, send_file
from flask.ext.discoverer import Discoverer, advertise
from functools import wraps

import logging
import socket
import sys
from time import sleep

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

clientIP = "127.0.0.1"
clientPORT = 27017
client = pymongo.MongoClient(clientIP, clientPORT)
client.drop_database("canvas")
client.drop_database("auth")
canvas = client.canvas
auth = client.auth
auth.pymongo.insert({"user": "user1", "password": "pass1"})
auth.pymongo.insert({"user": "user2", "password": "pass2"})
auth.pymongo.insert({"user": "user3", "password": "pass3"})

listOfColors = []

def on_service_state_change(zeroconf, service_type, name, state_change):
    print("Service %s of type %s state changed: %s" % (name, service_type, state_change))

    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        if info:
            print("  Address: %s:%d" % (socket.inet_ntoa(info.address), info.port))
            print("  Weight: %d, priority: %d" % (info.weight, info.priority))
            print("  Server: %s" % (info.server,))
            if info.properties:
                print("  Properties are:")
                for key, value in info.properties.items():
                    print("    %s: %s" % (key, value))
                    newList = value.decode()
                    listOfColors = newList.split(' ')
            else:
                print("  No properties")
        else:
            print("  No info")
        print('\n')


zeroconf = Zeroconf()
print("\nBrowsing services\n")

browser = ServiceBrowser(zeroconf, "_team18._tcp.local.", handlers=[on_service_state_change]) 
while len(listOfColors) < 1:
    sleep(0.1)
    
zeroconf.close()

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return auth.pymongo.find({"user": username, "password": password}).count()

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials.', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated



app = Flask(__name__)

@advertise(private=True, colors=[])
@app.route('/LED')
@requires_auth
def LED_route():
    print('LED route accessed')
    # do something
    return "LED"

@advertise(private=True, colors=[])
@app.route('/canvas')
def canvas_route():
    print('canvas route accessed')
    # do something
    return "canvas"

@advertise(private=True, colors=[])
@app.route('/hedgehogplz')
@requires_auth
def hedgehog_route():
    print('hedgehog route accessed')
    # do something
    return send_file('hedgebaby.jpg', mimetype='image/gif')

@advertise(private=True, colors=[])
@app.route('/catplz')
@requires_auth
def cat_route():
    print('cat route accessed')
    # do something
    return send_file('cat.jpg', mimetype='image/gif')
    
@advertise(private=True, colors=[])
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@requires_auth
def NULL_route(path):
    print ('NULL route accessed')
    return 'This is an invalid route, try harder next time.'

app.run(host='0.0.0.0', debug=True)
