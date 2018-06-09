#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "Text Files to Spreadsheet"
# from "Automate The Boring Stuff", by Al Sweigart,
# Chapter 12.
#
# "Write a program to read in the contents of several text 
# files (you can make the text files yourself) and insert those 
# contents into a spreadsheet, with one line of text per row. 
# The lines of the first text file will be in the cells of 
# column A, the lines of the second text file will be in the 
# cells of column B, and so on."
# 
# Nadia Borsch      misc@nborsch.com        Jun/2018

import openpyxl, os

print(f"\n{'Text Files to Spreadsheet':>40}")
print(f"{'~~~~ ~~~~~ ~~ ~~~~~~~~~~~':>40}")

# Get folder path from user
print(f"\nCurrent working directory is {os.getcwd()}:")
path = input("Please enter the desired folder path or leave blank to stay in current working directory.\n")
if path:
    os.chdir(path)

print(f"\nAll plain text files in {os.getcwd()} will be converted to a spreadsheet.")

# Set up workbook/worksheet
wb = openpyxl.Workbook()
sheet = wb.active

for foldername, subfolders, filenames in os.walk(path):
    for column, filename in enumerate(filenames, 1):
        print(f"Saving {filename} to spreadsheet...")

        try:
            txt_file = open(filename, "r")
        except IOError:
            print(f"Could not open {filename}.")
            continue
        
        try:
            lines = txt_file.readlines()
        except UnicodeDecodeError:
            print(f"{filename} is not a plain text file, skipped...")
            continue

        for row, line in enumerate(lines, 1):
            sheet.cell(column=column, row=row).value = line.strip("\n")

        txt_file.close()

# Save and close workbook
try:
    wb.save("txt2spreadsheet.xlsx")
except PermissionError:
    print("Could not save spreadsheet, please try again.")

print("Done.")
