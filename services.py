#!/usr/bin/env python3

from canvas import canvasAccessToken 
import pymongo
from flask import Flask, requests

clientIP = "127.0.0.1"
clientPORT = 27017
client = MongoClient(clientIP, clientPORT)
canvas = client.canvas
auth = client.auth
