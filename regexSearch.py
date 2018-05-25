#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "Regex Search"
# from "Automate The Boring Stuff", by Al Sweigart,
# Chapter 8.
#
# "Write a program that opens all .txt files in a folder and searches for any 
# line that matches a user-supplied regular expression. The results should be 
# printed to the screen."
# 
# Nadia Borsch      misc@nborsch.com        May/2018

import re, os, sys

print('{0:>30}'.format("----- ------"))
print('{0:>30}'.format("REGEX SEARCH"))
print('{0:>30}'.format("----- ------"))

# Ask for working directory
while True:
    askCwd = input(f"Current working directory is {os.getcwd()}.\nIs this the directory you'd like to use? (y/n)\n")
    if not askCwd or askCwd != 'y' and askCwd != 'n':
        print("Please enter y to use current directory or n to change to another directory.")
    elif askCwd == 'y':
        cwd = os.getcwd()
        break
    elif askCwd =='n':
        cwd = input("Please enter the absolute path for the directory you'd like to use.\n")
        break

# Validate working directory (escape, exists, etc)
if os.path.exists(cwd) == False and os.path.isdir(cwd) == False:
    print(f"The directory {os.path.basename(cwd)} doesn't exist.")
    sys.exit()
else:
    # Change to working directory
    os.chdir(cwd)

# Ask for regex
print(f"\nCurrent working directory is {cwd}.", end="")
while True:
    regex = re.compile(input("Please enter the regex you'd like to search for.\n"))
    if regex:
        break

# Find txt files
files = os.listdir(cwd)
txts = []

for file in files:
    if file.endswith(".txt"):
        txts.append(file)

# Open txt files and store filenames with matches
matches = []
for txt in txts:
    file = open(txt)
    content = file.read()
    if regex.search(content):
        matches.append(txt)
    file.close()
        
# Print results on screen
for match in matches:
    print(match)