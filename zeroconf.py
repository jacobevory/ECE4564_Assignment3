#!/usr/bin/env python

from zeroconf import ServiceInfo, Zeroconf

colors = {'Red', 'Yellow', 'Blue', 'Cyan', 'Green', 'White'}
name = 'team18led'
path = '' 
port = 5000
publish(name, colors, path, port)