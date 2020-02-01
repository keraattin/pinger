#!/usr/bin/env python3

import subprocess
import sys
from argparse import ArgumentParser

SUPPORTED_FILE_TYPES = ["xlsx","xls"]

# Ping command
def ping(host,count):
    try:
        cmd_ping = subprocess.check_output(["ping",host,"-c",str(count)])
        return True
    except subprocess.CalledProcessError:
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

#Check whether file type supported or not
def is_file_type_supported(file_format):
    if file_format in SUPPORTED_FILE_TYPES:
        return True
    else:
        return False

#Check whether is sheet index valid or not
def is_sheet_index_valid(sheet):    
    sheet_pattern = re.compile("[0-9]+") #Regex of sheet range
    if sheet_pattern.fullmatch(sheet):
        return True
    else:
        return False

#Processing arguments
def process_arguments(args):
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
        ip_column = int(args.column)
    else:
        ip_column = 0

    sheet = get_xlsx_rows(file_name,sheet_index)


def main():
    #Arguments
    parser = ArgumentParser(description="Ping hosts from files")
    parser.add_argument("-f","--filename", type=str, help="Column of ip addresses", required=True)
    parser.add_argument("-s","--sheet", default=0, help="Sheet index [default = 0]")
    parser.add_argument("-c","--column", default=0, help="Column of ip address [default = 0]")
    args = parser.parse_args()

    process_arguments(args)
    

if __name__ == "__main__":
    main()