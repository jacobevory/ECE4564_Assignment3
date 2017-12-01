#!/usr/bin/env python3
import requests
import re
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
import json

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf



listOfColors = []

updateColor = ""
updateIntensity = ""
updateStatus = ""

currentColor = ""
currentStatus = ""

LEDaddress = "172.29.18.24:5000"

def on_service_state_change(zeroconf, service_type, name, state_change):
    print("Service %s of type %s state changed: %s" % (name, service_type, state_change))
    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        if info:
            #LEDaddress = info.address.decode() + ':' + info.port.decode()
            print("  Address: %s:%d" % (socket.inet_ntoa(info.address), info.port))
            print("  Weight: %d, priority: %d" % (info.weight, info.priority))
            print("  Server: %s" % (info.server))
            if info.properties:
                print("  Properties are:")
                for key, value in info.properties.items():
                    newList = value.decode()                    
                    listOfColors.append(newList.split())
                    print(" ", listOfColors)
            else:
                print("  No properties")
        else:
            print("  No info")
        print('\n')


zeroconf = Zeroconf()
print("\nBrowsing services\n")
browser = ServiceBrowser(zeroconf, "_team18._tcp.local.", handlers=[on_service_state_change]) 

while listOfColors == []:
    sleep(0.1)
    
zeroconf.close()
'''
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
'''
app = Flask(__name__)

@advertise(private=True, colors=[], method=['GET', 'POST'])
@app.route('/LED')
#@requires_auth
def LED_route():
    print('LED route accessed')
    # do something
    if request.method == 'POST':
        updateStatus = str(request.get_json().get('status'))
        updateIntensity = str(request.get_json().get('intensity'))
        updateColor = str(request.get_json().get('color'))                           
        newStatus = {'status': updateStatus, 'intensity': updateIntensity, 'color': updateColor}        
        r = requests.post("http://" + LEDaddress + "/LED", json.dumps(newStatus))
        return r.text
    elif request.method == 'GET':        
        r = requests.get("http://" + LEDaddress + "/LED") 
        #currentStatus = str(r.json().get('ledStatus').get('status'))
        #currentColor = str(r.json().get_json().get('ledStatus').get('color'))
        return r.json()
'''
@advertise(private=True, colors=[], method=['GET', 'POST'])
@app.route('/Canvas')
def canvas_route():
    print('canvas route accessed')   
    status = str(request.args.get('file'))
    # do something
    if request.method == 'POST':
        access_token = canvasAccessToken
        filename = status
        api_url='https://canvas.vt.edu/api/v1/groups/46402/files'
        session = requests.Session()
        session.headers = {'Authorization': 'Bearer %s' % access_token}
        payload = {}
        payload['name'] = filename
        payload['parent_folder_path'] = '/'
        uploadr = session.post(api_url, data=payload)
        uploadr.raise_for_status()
        uploadr = uploadr.json()
        payload = list(uploadr['upload_params'].items())
        with open(filename, 'rb') as f:
             file_content=f.read()
        payload.append((u'file', file_content))
        uploadr = requests.post(uploadr['upload_url'], files=payload)
        uploadr.raise_for_status()
        uploadr = uploadr.json()
    if request.method == 'GET':
        filename=status
        url="url"
        token=canvasAccessToken
        url = "https://vt.instructure.com/api/v1/groups/46402/files?access_token=" + token
        r=requests.get(url)
        data = r.content.decode()
        datas = data.split('{')

        i=0; 
        while i < len(datas):
           lines = datas[i].split(',')
           if any(filename in s for s in lines):
              temp=filter(lambda x: 'url' in x, lines)
              strtemp = ''.join(temp)
              urls = re.search("(?P<url>https?://[^\s]+)", strtemp).group("url")
              rest = urls.split('"', 1)[0]
              finalurl = rest.replace("\u0026", "&")
              r = requests.get(finalurl, allow_redirects=True)
              open(filename, 'wb').write(r.content)
           i+=1
        return send_file(filename)
'''
@advertise(private=True, colors=[])
@app.route('/hedgehogplz')
#@requires_auth
def hedgehog_route():
    print('hedgehog route accessed')
    # do something
    return send_file('hedgebaby.jpg', mimetype='image/gif')

@advertise(private=True, colors=[])
@app.route('/catplz')
#@requires_auth
def cat_route():
    print('cat route accessed')
    # do something
    return send_file('cat.jpg', mimetype='image/gif')

@advertise(private=True, colors=[])
@app.route('/simonsays', methods=['POST'])
#@requires_auth
def simon_route():
    txt = request.form['simonsays']
    if not txt.startswith('Simon says'):
        print("You did not say Simon says")
        return "You did not say Simon says"
    txt = txt.replace('Simon says', '')
    print(txt)
    return txt

@advertise(private=True, colors=[])
@app.route('/liftoff', methods=['POST'])
#@requires_auth
def liftoff_route():
    txt = request.form['start']
    i = int(txt)
    while i > 0:
        print(i)
        i = i - 1
        sleep(1)
    return "We have lift off"

@advertise(private=True, colors=[])
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
#@requires_auth
def NULL_route(path):
    print ('NULL route accessed')
    return 'This is an invalid route, try harder next time.'

app.run(host='0.0.0.0', debug=True)
