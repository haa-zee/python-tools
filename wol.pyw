#!/usr/bin/python

from socket import *
import sys,os

if len(sys.argv)<2:
    raise ValueError("MAC address missing...")
mac_addr=sys.argv[1]


if len(sys.argv)>2:
    ip_broadcast=sys.argv[2]
else:
    if os.name == "nt":
        print '''You're using a Windows system and the broadcast address is missing.
If you have more than one network interface, the WoL packet
could go in a wrong direction.

If the routing table contains more than one entry for 255.255.255.255,
the packet will go out on interface which has lower metrics'''
        raw_input("Press <Enter> to continue...")
        
    ip_broadcast='255.255.255.255'  # It works on linux, but not on Windows!
    


so=socket(AF_INET, SOCK_DGRAM)
magic="\xff"*6+mac_addr.replace(':','').decode('hex')*16
so.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
so.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
so.sendto(magic, (ip_broadcast,9))
