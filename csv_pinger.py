#!/usr/bin/env python3

import subprocess
import ping
import sys
import colors

def get_csv_rows(file_name):
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
            total_unreachable +=1
            print(f"{colors.LIGHT_RED}{addr:<20}{'[-][FAIL]':<12}{colors.NC}")
        
    print("Total Reachable : {}".format(str(total_reachable)))
    print("Total Unreachable : {}".format(str(total_unreachable)))