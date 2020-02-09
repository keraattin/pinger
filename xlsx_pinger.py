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

def get_xlsx_rows(file_name,sheet_index):
    #Import xlrd library for read xlsx files
    try:
        import xlrd
    except:
        #If library not exist install library
        subprocess.call(["pip3","install","xlrd"])
    
    #Open Workbook
    try:
        wb = xlrd.open_workbook(file_name)
    except:
        print("Wrong file name")
        sys.exit(-1) #Exit with error code
    
    try:
        sheet = wb.sheet_by_index(sheet_index)
    except:
        print("Number of index [{}] not found".format(sheet_index))
        sys.exit(-1) #Exit with error code
    
    return sheet #Returning rows

def get_all_sheets(file_name):
    #Import xlrd library for read xlsx files
    try:
        import xlrd
    except:
        #If library not exist install library
        subprocess.call(["pip3","install","xlrd"])
    
    #Open Workbook
    try:
        wb = xlrd.open_workbook(file_name)
    except:
        print("Wrong file name")
        sys.exit(-1) #Exit with error code
    
    return wb

def run(sheet,ip_column,ping_count):
    total_reachable = 0
    total_unreachable = 0
    for i in range(1,sheet.nrows):
        addr = sheet.cell_value(i,ip_column)
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
def autorun(wb,ping_count):
    sheet_list = wb.sheet_names() #Getting Sheet List

    total_reachable = 0
    total_unreachable = 0
    
    for s_name in sheet_list:
        sheet = wb.sheet_by_name(str(s_name)) #Getting all sheets one by one

        for i in range(0,sheet.nrows):
            for j in range(0,sheet.ncols):
                cell_value = sheet.cell_value(i,j) #Getting every cells one by one

                if is_cell_value_is_ip_v4_address(cell_value): #Checking whether cell is an ip v4 address or not
                    if ping.ping(cell_value,ping_count):
                        total_reachable += 1
                        print(f"{colors.LIGHT_GREEN}{cell_value:<20}{'[+][OK]':<12}{colors.NC}")
                    else:
                        tcp_port = ping.check_tcp_ports(cell_value) #Checking Tcp ports
                        if tcp_port:
                            total_reachable += 1
                            print(f"{colors.LIGHT_GREEN}{cell_value:<20}{'[+][OK][Port:{}]'.format(str(tcp_port)):<12}{colors.NC}")
                        else:
                            total_unreachable +=1
                            print(f"{colors.LIGHT_RED}{cell_value:<20}{'[-][FAIL]':<12}{colors.NC}")
    
    print("Total Reachable : {}".format(str(total_reachable)))
    print("Total Unreachable : {}".format(str(total_unreachable)))

