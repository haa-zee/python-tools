#!/usr/bin/python

from socket import *
import sys
import argparse
import socket
import re



class Mac_addr(object):
# Temporary class - will be imported from my own package
    def __init__(self,mac_string):
        self.set_mac_addr(mac_string)

    def set_mac_addr(self, mac_string):
        self._mac_addr=self.__pack_mac(mac_string)

    def __pack_mac(self, mac_string):
        _mac=mac_string.strip().upper()
        if re.match("^(([0-9A-F]{2}:){5}[0-9A-F]{2}|[0-9A-F]{12})$",_mac):
            return long(_mac.replace(":",""),16)
        else:
            raise ValueError("Invalid MAC address")

    def get_mac_addr(self):
        return self._mac_addr

    def __str__(self):
        str_mac="%012X"%(self._mac_addr)
        return ":".join([str_mac[i:i+2] for i in xrange(0,len(str_mac),2)])


class IP_addr(object):
# Temporary class - will be imported from my own package
    def __init__(self, ip_addr):
        try:
            self._ip=socket.inet_aton(ip_addr)
        except socket.error as e:
            raise ValueError("Illegal IP address")

    def get_addr(self):
        return self._ip

    def __str__(self):
        return str(socket.inet_ntoa(self.get_addr()))

class ParsedArguments(object):
    # this class used as container for runtime arguments
    # (instead of a global variable)
    pass


def send_magic_packet(mac_address, broadcast_address="255.255.255.255"):
    so=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    magic="\xff"*6+mac_address.replace(':','').decode('hex')*16
    so.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    so.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    so.sendto(magic, (broadcast_address,9))

def send_message_if_interactive(msgtext):
    if ParsedArguments.interactive:
        return raw_input(msgtext)

parser=argparse.ArgumentParser()
# positional paramter MAC address and IP broadcast address
parser.add_argument("mac",action='store',type=Mac_addr,help="MAC address")
parser.add_argument("broadcast",action='store',nargs='?',default='255.255.255.255',type=IP_addr)
parser.add_argument("-i","--interactive",action='store_true')

parser.parse_args(namespace=ParsedArguments)

mac_addr=str(ParsedArguments.mac)
broadcast=str(ParsedArguments.broadcast)

if sys.platform in ('cygwin','win32') and broadcast == "255.255.255.255":
        print '''
You're using a Windows system and the broadcast address is %s.
If you have more than one network interface, the WoL packet
could go in a wrong direction.

If the routing table contains more than one entry for 255.255.255.255,
the packet will go out on interface which has lower metrics'''%(broadcast,)
        send_message_if_interactive("Press <Enter> to continue...\n\n")
        

send_magic_packet(mac_addr, broadcast)

print "WOL sent to MAC %s broadcast address %s"%(mac_addr, broadcast)
send_message_if_interactive("Press <Enter> to continue...")

