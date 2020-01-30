#!/usr/bin/env python3

import subprocess
import sys
from argparse import ArgumentParser

# Ping command
def ping(host,count):
    try:
        cmd_ping = subprocess.check_output(["ping",host,"-c",str(count)])
        return True
    except subprocess.CalledProcessError:
        return False

def xlsx_process(file_name,sheet_index):
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

def main():
    #Arguments
    parser = ArgumentParser(description="Ping hosts from files")
    parser.add_argument("-f","--filename", type=str, help="Column of ip addresses", required=True)
    parser.add_argument("-s","--sheet", default=0, help="Sheet index[default = 0]")
    args = parser.parse_args()

    #File Name
    if args.filename:
        file_name = str(args.filename)
    else:
        print("File name and sheet must be entered.")

    #Sheet Index
    if args.sheet:
        sheet_index = int(args.sheet)
    else:
        sheet_index = 0

    xlsx_process(file_name,sheet_index)

if __name__ == "__main__":
    main()