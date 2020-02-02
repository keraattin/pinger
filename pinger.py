#!/usr/bin/env python3

import sys
from argparse import ArgumentParser
import re
import xlsx_pinger

SUPPORTED_FILE_TYPES = ["xlsx","xls"]

#Check whether file type supported or not
def is_file_type_supported(file_format):
    if file_format in SUPPORTED_FILE_TYPES:
        return True
    else:
        return False

#Check whether sheet index valid or not
def is_sheet_index_valid(sheet):    
    sheet_pattern = re.compile("[0-9]+") #Regex of sheet column
    if sheet_pattern.fullmatch(str(sheet)):
        return True
    else:
        return False

#Check whether ip column index valid or not
def is_ip_column_index_valid(ip_column):
    ip_column_pattern = re.compile("[0-9]+") #Regex of ip address column
    if ip_column_pattern.fullmatch(str(ip_column)):
        return True
    else:
        return False

#Check whether ping request count valid or not
def is_ping_count_valid(ping_count):    
    ping_count_pattern = re.compile("[0-9]+") #Regex of ping count
    if ping_count_pattern.fullmatch(str(ping_count)):
        return True
    else:
        return False

def main():
    #Arguments
    parser = ArgumentParser(description="Ping hosts from files")
    parser.add_argument("-f","--filename", type=str, help="Column of ip addresses", required=True)
    parser.add_argument("-s","--sheet", type=int, default=0, help="Sheet index [default = 0]")
    parser.add_argument("-c","--column", type=int, default=0, help="Column of ip address [default = 0]")
    parser.add_argument("-pc","--pingcount", type=int, default=3, help="How many times sending ping request [default = 3]")
    args = parser.parse_args()

    #File Name
    if args.filename:
        file_name = str(args.filename)
        file_format = file_name.split('.')[-1]
        if not is_file_type_supported(file_format):
            print("{} file format not supported".format(file_format))
            sys.exit(-1) #Exit with error code
    else:
        print("File name and sheet must be entered.")
        sys.exit(-1) #Exit with error code
        
    #Sheet Index
    if args.sheet:
        if is_sheet_index_valid(args.sheet):
            sheet_index = int(args.sheet)
        else:
            print("You entered wrong sheet index")
            sys.exit(-1) #Exit with error code
    else:
        sheet_index = 0
    
    #Column of ip address
    if args.column:
        if is_ip_column_index_valid(args.column):
            ip_column = int(args.column)
        else:
            print("You entered wrong ip column index")
            sys.exit(-1) #Exit with error code
    else:
        ip_column = 0
    

    #Ping Count
    if args.pingcount:
        if is_ping_count_valid(args.pingcount):
            ping_count = int(args.pingcount)
        else:
            print("You entered wrong ping count value")
            sys.exit(-1) #Exit with error code
    else:
        ping_count = 3

    sheet = xlsx_pinger.get_xlsx_rows(file_name,sheet_index) #Get sheet

    xlsx_pinger.run(sheet,ip_column,ping_count) #Run pinger
    

if __name__ == "__main__":
    main()