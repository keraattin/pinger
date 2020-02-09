#!/usr/bin/env python3

import subprocess
import ping
import sys
import re
import colors

#Check whether cell value is an ip v4 address or not
def is_cell_value_is_ip_v4_address(cell_value):    
    #Regex of ip v4 address
    ip_v4_pattern = re.compile("(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])")
    if ip_v4_pattern.fullmatch(str(cell_value)):
        return True
    else:
        return False

def get_csv_document(file_name):
    #Import xlrd library for read xlsx files
    try:
        import csv
    except:
        #If library not exist install library
        subprocess.call(["pip3","install","csv"])
    
    try:
        csvfile = open(file_name)
        csv_document = csv.reader(csvfile)
        return csv_document
    except:
        print("Wrong file name")
        sys.exit(-1) #Exit with error code
    
def run(csv_document,ip_column,ping_count):
    total_reachable = 0
    total_unreachable = 0
    
    list_iterator = iter(csv_document)
    next(list_iterator) #Skip header column

    for row in list_iterator:
        addr = row[ip_column]
        if ping.ping(addr,ping_count):
            total_reachable += 1
            print(f"{colors.LIGHT_GREEN}{addr:<20}{'[+][OK]':<12}{colors.NC}")
        else:
            tcp_port = ping.check_tcp_ports(addr) #Checking Tcp ports
            if tcp_port:
                total_reachable += 1
                print(f"{colors.LIGHT_GREEN}{addr:<20}{'[+][OK][Port:{}]'.format(str(tcp_port)):<12}{colors.NC}")
            else:
                total_unreachable +=1
                print(f"{colors.LIGHT_RED}{addr:<20}{'[-][FAIL]':<12}{colors.NC}")
        
    print("Total Reachable : {}".format(str(total_reachable)))
    print("Total Unreachable : {}".format(str(total_unreachable)))

#Getting whole cells in document,
#Check whether is an ip address or not,
#Check whether host is up or not
def autorun(csv_document,ping_count):
    total_reachable = 0
    total_unreachable = 0

    for row in csv_document:
        for cell in row:
            if is_cell_value_is_ip_v4_address(cell): #Checking whether cell is an ip v4 address or not
                if ping.ping(cell,ping_count):
                    total_reachable += 1
                    print(f"{colors.LIGHT_GREEN}{cell:<20}{'[+][OK]':<12}{colors.NC}")        
                else:
                    tcp_port = ping.check_tcp_ports(cell) #Checking Tcp ports
                    if tcp_port:
                        total_reachable += 1
                        print(f"{colors.LIGHT_GREEN}{cell:<20}{'[+][OK][Port:{}]'.format(str(tcp_port)):<12}{colors.NC}")
                    else:
                        total_unreachable +=1
                        print(f"{colors.LIGHT_RED}{cell:<20}{'[-][FAIL]':<12}{colors.NC}")
    
    print("Total Reachable : {}".format(str(total_reachable)))
    print("Total Unreachable : {}".format(str(total_unreachable)))