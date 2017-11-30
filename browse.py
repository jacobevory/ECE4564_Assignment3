#!/usr/bin/env python3

import logging
import socket
import sys
from time import sleep

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

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
