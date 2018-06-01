#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "Filling in the Gaps (Challenge)"
# from "Automate The Boring Stuff", by Al Sweigart,
# Chapter 9.
#
# "Write a program that finds all files with a given prefix, such as spam001.txt, 
# spam002.txt, and so on, in a single folder and locates any gaps in the numbering 
# (such as if there is a spam001.txt and spam003.txt but no spam002.txt). Have the 
# program rename all the later files to close this gap.
# 
# As an added challenge, write another program that can insert gaps into numbered 
# files so that a new file can be added."
# 
# Nadia Borsch      misc@nborsch.com        May/2018

import os, shutil

print("")
print('{:>45}'.format("FILLING THE GAPS CHALLENGE"))
print('{:>45}'.format("------- --- ---- ---------"))

# Obtain folder path from user
while True:
    folder_path = os.path.abspath(input("Please enter the path for the folder where files are located.\n"))
    if not os.path.exists(folder_path):
        print(f"{folder_path} doesn't exist.")
    else:
        break

os.chdir(folder_path)
print(f"\nCurrent working directory is {folder_path}.\n")

# Obtain files prefix
while True:
    prefix = input(f"Please enter the prefix of the files to be re-numbered.\n")
    if prefix:
        break

print(f"\nFile prefix is {prefix}.\n")

# Obtain number of gaps
while True:
    try:
        gaps_number = int(input(f"Please enter the number of gaps to be inserted.\n"))
        if gaps_number <= 0:
            print("Please enter a positive number greater than zero.")
        elif gaps_number > 0:
            break
    except ValueError:
        print("\nPlease enter a number.")

# Obtain last properly named file
while True:
    try:
        gaps_start = int(input(f"\nPlease enter from which number files should be renamed.\n"))
        if gaps_start:
            break
    except ValueError:
        print("\nPlease enter a number.")

print(f"{gaps_number} gaps will be inserted starting from file #{gaps_start}.")

# Go through each file in folder, find all numbered filenames, and store names in list
numbered_files = []
for foldername, subfolders, filenames in os.walk(folder_path):
    for filename in filenames:
        if filename.startswith(prefix):
            numbered_files.append(filename)

# Create list with files to be renamed
if gaps_start == 0:
    rename_files = numbered_files[gaps_start : len(numbered_files)]
else:
    rename_files = numbered_files[gaps_start - 1: len(numbered_files)]

rename_files = rename_files[::-1]
number_files = len(rename_files)

# Rename files
for file in rename_files:
    suffix = file.split(".")
    print(f"Renaming {file} to {prefix}{number_files + gaps_number + gaps_start - rename_files.index(file) - 1}.{suffix[1]}...")
    shutil.move(f"{folder_path}\{file}", f"{folder_path}\{prefix}{number_files + gaps_number + gaps_start - rename_files.index(file) - 1}.{suffix[1]}")
