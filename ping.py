#!/usr/bin/env python3

import subprocess
import time

#Import Scapy library
try:
    from scapy.all import *
except:
    #If library not exist install library
    subprocess.call(["pip3","install","scapy"])

TOP_TCP_PORTS = [22,53,80,443,3306,8080]

# Ping command
def ping(host,count):
    time_out = 1
    icmp_pkg = IP(dst=host)/ICMP()
    response = sr1(icmp_pkg,verbose=False,timeout=time_out)
    if not (response is None):
        return True
    else:
        return False

#Check whether tcp ports are open or not with syn, syn+ack
def check_tcp_ports(host):
    src_port = RandNum(1024,65535) #Random Source Port
    seq_num = RandNum(150000,160000) #Random Sequence Number
    time_out = 1
    
    for dst_port in TOP_TCP_PORTS:
        try:
            syn_pkg = IP(dst=host)/TCP(sport=src_port,dport=dst_port,seq=seq_num,flags="S")
            syn_ack = sr1(syn_pkg,verbose=False,timeout=time_out)
            pkgflags = syn_ack.getlayer(TCP).flags
            if pkgflags == "SA": #SynAck
                return dst_port         
        except:
            pass
    return False #Not found any open tcp port