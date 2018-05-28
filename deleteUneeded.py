#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "Deleting Unneeded Files"
# from "Automate The Boring Stuff", by Al Sweigart,
# Chapter 9.
#
# "Write a program that walks through a folder tree and searches for exceptionally 
# large files or folders—say, ones that have a file size of more than 100MB. 
# (Remember, to get a file’s size, you can use os.path.getsize() from the os module.) 
# Print these files with their absolute path to the screen."
# 
# Nadia Borsch      misc@nborsch.com        May/2018

import os, shutil

print("")
print('{:>40}'.format("SEARCH FILES OVER 100mb"))
print('{:>40}'.format("------ ----- ---- -----"))

# Obtain folder tree path from user
while True:
    tree_path = os.path.abspath(input("Please enter the path for the folder you want to search in.\n"))
    if not os.path.exists(tree_path):
        print(f"{tree_path} doesn't exist.")
    else:
        break

os.chdir(tree_path)
print(f"\n{tree_path} will be searched for files over 100MB in size.\n")

# Storage for names of files over 100MB
big_files = []

# Go through each folder and check size of each file
for foldername, subfolders, filenames in os.walk(tree_path):
    print(f"Searching {foldername} for files over 100MB...")

    for filename in filenames:
        if os.path.getsize(f"{foldername}\{filename}") > 10**7:
            big_files.append(f"{foldername}\{filename}")

# Ask user which way to provide results
print("\nSearch is done.")
while True:
    choice = input(f"Would you like to save results to a file (f) or have them shown on the screen (s)?\n").lower()
    if choice == "f" or choice == "s":
        break

# Save results to file
if choice == "f":
    choice_file = open("big_files.txt", "w")
    for big_file in big_files:
        choice_file.write(f"{big_file}\n")
    choice_file.close()
    print(f"\nFile big_files.txt saved to {tree_path}.\n")

# Show results on screen
elif choice == "s":
    print("\nThe following files are over 100MB in size:\n")
    for big_file in big_files:
        print(f"{big_file}")

