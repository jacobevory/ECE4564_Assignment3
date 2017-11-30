#!/usr/bin/env python3

from flask import Flask, request
import RPi.GPIO as GPIO
import time
import zeroconf
import socket
import json


server = zeroconf.Zeroconf()
 
# Get local IP address
local_ip = socket.gethostbyname(socket.gethostname())
local_ip = socket.inet_aton(local_ip)
svc1 = zeroconf.ServiceInfo('_team18._tcp.local.', 'colors._team18._tcp.local.', address = local_ip, port = 2972, weight = 0, priority=0, properties = {'colors': 'red blue green magenta cyan yellow white'})
server.register_service(svc1)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(12,GPIO.OUT) #red led
GPIO.setup(16,GPIO.OUT) #blue led
GPIO.setup(18,GPIO.OUT) #yellow led

red = GPIO.PWM(12, 50)
blue = GPIO.PWM(16, 50)
green = GPIO.PWM(18, 50)

app = Flask(__name__)

status = ''
color = ''
intensity = ''

@app.route('/LED', methods=['GET', 'POST'])
def LED():
    if request.method == 'POST':
        print('Changing LED')
        global status
        status = str(request.args.get('status'))
        print('Changing status to ' + status)
        if status == 'off':
            return "LED off"
        elif status != 'on':
            print('Error: Status incorrect.')
            print('Correct options are on or off.')
            return "LED not changed due to error."

        global color
        color = str(request.args.get('color'))
        print('Changing color to ' + color)
        if color == 'red':
            red.start(100)
            blue.stop()
            green.stop()
        elif color == 'blue':
            red.stop()
            blue.start(100)
            green.stop()
        elif color == 'yellow':
            red.start(100)
            blue.stop()
            green.start(100)
        elif color == 'magenta':
            red.start(100)
            blue.start(100)
            green.stop()
        elif color == 'cyan':
            red.stop()
            blue.start(100)
            green.start(100)
        elif color == 'green':
            red.stop()
            blue.stop()
            green.start(100)
        elif color == 'white':
            red.start(100)
            blue.start(100)
            green.start(100)
        else:
            print('Error: Color incorrect.')
            print('Correct options are: magenta, white, green, cyan, yellow, blue, red.')
            return "LED not changed due to error."

        global intensity
        intensity = str(request.args.get('intensity'))
        print('Changing intensity to ' + intensity)
        inten = int(intensity)
        if inten >= 0 & inten <= 100:
            red.ChangeDutyCycle(inten)
            blue.ChangeDutyCycle(inten)
            green.ChangeDutyCycle(inten)
        else:
            print('Error: Intensity incorrect.')
            print('Correct options are >= 0 and <= 100.')
            return "LED not changed due to error."
        return "LED changed"

    elif request.method == 'GET':
        newStatus = {'status': status, 'color': color}
        print('Sent POST request with status and color')
        return json.dumps(newStatus), 201


app.run(host='0.0.0.0', debug=True)

GPIO.cleanup()
