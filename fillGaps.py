#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "Filling in the Gaps (challenge)"
# from "Automate The Boring Stuff", by Al Sweigart,
# Chapter 9.
#
# "Write a program that finds all files with a given prefix, such as spam001.txt, 
# spam002.txt, and so on, in a single folder and locates any gaps in the numbering 
# (such as if there is a spam001.txt and spam003.txt but no spam002.txt). Have the 
# program rename all the later files to close this gap."
# 
# Nadia Borsch      misc@nborsch.com        May/2018

import os, shutil

print("")
print('{:>40}'.format("FILLING THE GAPS"))
print('{:>40}'.format("------- --- ----"))

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
    prefix = input(f"Please enter the prefix to be searched.\n")
    if prefix:
        break

ordered_files = []

# Go through each file in folder, check if names match, and store 
for foldername, subfolders, filenames in os.walk(folder_path):
    for filename in filenames:
        if filename.startswith(prefix):
            ordered_files.append(filename)

# If there is a gap, find next files and rename them
for file in ordered_files:
    ordered_prefix = prefix + str(ordered_files.index(file) + 1)
    
    # Get file suffix
    suffix = file.split(".")

    # Find gaps
    if file.startswith(ordered_prefix):
        continue
    else:
        # Inform user of gap found
        print(f"Renaming {file} to {ordered_prefix}.{suffix[1]}...")
        #Rename file
        shutil.move(f"{file}", f"{ordered_prefix}.{suffix[1]}")

print("Done.")