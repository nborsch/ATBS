#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "Excel-to-CSV Converter"
# from "Automate The Boring Stuff", by Al Sweigart,
# Chapter 14.
#
# "Excel can save a spreadsheet to a CSV file with a few mouse clicks, 
# but if you had to convert hundreds of Excel files to CSVs, it would 
# take hours of clicking. Using the openpyxl module from Chapter 12, 
# write a program that reads all the Excel files in the current working 
# directory and outputs them as CSV files. 
# 
# A single Excel file might contain multiple sheets; you’ll have to 
# create one CSV file per sheet. The filenames of the CSV files should 
# be <excel filename>_<sheet title>.csv, where <excel filename> is the 
# filename of the Excel file without the file extension (for example, 
# 'spam_data', not 'spam_data.xlsx') and <sheet title> is the string 
# from the Worksheet object’s title variable."
# 
# Nadia Borsch      misc@nborsch.com        Jun/2018

import os, openpyxl, csv

print(f"\n{'Spreadsheet To CSV':>35}")
print(f"{'=========== == ===':>35}")

# Get folder path from user
print(f"\nCurrent working directory is {os.getcwd()}:")
path = input("Please enter the desired folder path or leave blank to stay in current working directory.\n")
if path:
    os.chdir(path)
else:
    path = "."

# Loop through all workbook files
for workbook in os.listdir(path):
    # Skip files that are not spreadsheet files
    if not workbook.endswith(".xlsx"):
        continue
    
    print(f"Opening {workbook}...")
    wb = openpyxl.load_workbook(workbook)

    # Loop through all worksheets in current workbook
    for worksheet_name in wb.sheetnames:
        worksheet = wb[worksheet_name]
        csv_file = open(f"{workbook.rstrip('.xlsx')}_{worksheet_name}.csv", "w", newline="", encoding="UTF-16")
        csv_writer = csv.writer(csv_file)
        print(f"Working through sheet {worksheet_name}...")
        
        # Loop through every row in current worksheet
        for row in range(1, worksheet.max_row + 1):
            row_data = []
            
            # Loop through every cell in current row
            for column in range(1, worksheet.max_column + 1):
                row_data.append(worksheet.cell(row=row, column=column).value)
                
            # Write current row in csv file
            csv_writer.writerow(row_data)
        
        csv_file.close()
        print(f"Saved {workbook.rstrip('.xlsx')}_{worksheet_name}.csv.\n")

print("Done.")
