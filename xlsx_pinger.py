#!/usr/bin/env python3

import subprocess
import ping

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

def run(sheet,ip_column):
    total_reachable = 0
    total_unreachable = 0
    for i in range(1,sheet.nrows):
        addr = sheet.cell_value(i,ip_column)
        if ping.ping(addr):
            total_reachable += 1
            print(f"{addr:<20}{'[OK][+]':>12}")
        else:
            total_unreachable +=1
            print(f"{addr:<20}{'[FAIL][-]':>12}")
        
    print("Total Reachable : {}".format(str(total_reachable)))
    print("Total Unreachable : {}".format(str(total_unreachable)))