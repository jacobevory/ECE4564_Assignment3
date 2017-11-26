#!/usr/bin/env python

from zeroconf import ServiceInfo, Zeroconf

colors = {'Red', 'Yellow', 'Blue', 'Cyan', 'Green', 'White'}
name = 'team18led'
path = '' 
port = 5000
publish(name, colors, path, port)

#maybe another way:
'''
import Zeroconf
import socket
 
server = Zeroconf.Zeroconf()
 
# Get local IP address
local_ip = socket.gethostbyname(socket.gethostname())
local_ip = socket.inet_aton(local_ip)


colors = {'Red', 'Yellow', 'Blue', 'Cyan', 'Green', 'White'}
 
svc1 = Zeroconf.ServiceInfo('_team18led._tcp.local.', 'Colors._team18led._tcp.local.', address = local_ip, port = 2972, weight = 0, priority=0, properties = {'Colors': colors})
server.registerService(svc1)

'''
