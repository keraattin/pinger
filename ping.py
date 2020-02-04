#!/usr/bin/env python3

import subprocess

#Import Scapy library
try:
    from scapy.all import *
except:
    #If library not exist install library
    subprocess.call(["pip3","install","scapy"])

TOP_TCP_PORTS = [21,22,23,25,53,80,110,139,143,443,993,995,3306,8080]

# Ping command
def ping(host,count):
    try:
        cmd_ping = subprocess.check_output(["ping",host,"-c",str(count)])
        return True
    except subprocess.CalledProcessError:
        return False
