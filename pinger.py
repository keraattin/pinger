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
    try:
        import re
    except:
        subprocess.call(["pip3","install","re"])
    
    sheet_pattern = re.compile("[0-9]+(-[0-9]+)?") #Regex of sheet range
    if sheet_pattern.fullmatch(sheet):
        return True
    else:
        return False

#Define start and end index of sheet
def define_start_and_end_sheet_index(sheet_index):
    #[0] = Start Index
    #[1] = End Index
    sheet_index_list = [0,0]
    if "-" in sheet_index:
        sheet_index_list[0] = int(sheet_index.split('-')[0]) #Start Index
        sheet_index_list[1] = int(sheet_index.split('-')[1]) #Stop Index
    else:
        sheet_index_list[0] = sheet_index_list[1] = int(sheet_index)
    
    return sheet_index_list

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
        if not is_sheet_index_valid(args.sheet):
            print("You entered wrong sheet index")
            sys.exit(-1) #Exit with error code
        sheet_index_list = define_start_and_end_sheet_index(args.sheet)
        print("Start : {}".format(str(sheet_index_list[0])))
        print("End : {}".format(str(sheet_index_list[1])))
    else:
        sheet_index_list = define_start_and_end_sheet_index(args.sheet)
        print("Start : {}".format(str(sheet_index_list[0])))
        print("End : {}".format(str(sheet_index_list[1])))
    
    #Column of ip address
    if args.column:
        ip_column = int(args.column)
    else:
        ip_column = 0

    #sheet = get_xlsx_rows(file_name,sheet_index)
    

def run(sheet,ip_column):
    for i in range(1,sheet.nrows):
        ip_address = sheet.cell_value(i,ip_column)
        ping(ip_address,4)

def main():
    #Arguments
    parser = ArgumentParser(description="Ping hosts from files")
    parser.add_argument("-f","--filename", type=str, help="Column of ip addresses", required=True)
    parser.add_argument("-s","--sheet", default="0", help="Sheet index [default = 0]")
    parser.add_argument("-c","--column", default=0, help="Column of ip address [default = 0]")
    args = parser.parse_args()

    process_arguments(args)
    

if __name__ == "__main__":
    main()