#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "Selective Copy"
# from "Automate The Boring Stuff", by Al Sweigart,
# Chapter 9.
#
# "Write a program that walks through a folder tree and searches 
# for files with a certain file extension (such as .pdf or .jpg). 
# Copy these files from whatever location they are in to a new folder."
# 
# Nadia Borsch      misc@nborsch.com        May/2018

import os, shutil, re

print('{:>30}'.format("SELECTIVE FILE COPY"))
print('{:>30}'.format("--------- ---- ----"))

# Obtain source path from user
while True:
    source_path = os.path.abspath(input("Please enter the path for the source folder.\n"))
    if source_path:
        break

os.chdir(source_path)
print(f"\nFiles will be copied from {source_path}.\n")

# Obtain destination path from user
while True:
    dest_path = os.path.abspath(input("Please enter the path for the source folder.\nFolder will be created if it doesn't already exist.\n"))
    if dest_path:
        break

if not os.path.exists(dest_path):
    os.makedirs(dest_path)

print(f"\nFiles will be copied to {dest_path}.\n")

# Obtain extension from user
while True:
    file_ext = input("Please enter the extension (.ext) for the type of files you want to copy.\n")
    if file_ext:
        if file_ext.startswith("."):
            break
        else:
            file_ext = "." + file_ext
            break

print(f"\nFiles with the extension \"{file_ext}\" will be copied.\n")

# Create regex from extension provided
regex = re.compile(f"^(.+)({file_ext})")

# Walk folder tree
for foldername, subfolders, filenames in os.walk(source_path):
    print(f"Searching files in {foldername}...")
    
    # Find files with extension and list them
    for filename in filenames:
        if regex.search(filename):
            try:
                # Copy found files
                print(f"Copying {filename}...")
                shutil.copy(f"{foldername}\{filename}", f"{dest_path}")
            except shutil.SameFileError:
                # Continue operation if files are the same in source and destination
                continue
        else:
            continue

print('Done.')