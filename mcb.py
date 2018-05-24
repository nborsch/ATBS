#! python3
# -*- coding: utf-8 -*-
#
# My version of Practice Project "Extending the Multiclipboard"
# from "Automate The Boring Stuff", by Al Sweigart,
# Chapter 8.
# 
# Nadia Borsch      misc@nborsch.com        May/2018

import shelve, pyperclip

mcbShelf = shelve.open('mcb')
usageInfo = ('Usage:\tsave <keyword> - Saves clipboard to keyword.\n\t<keyword> - Loads keyword to clipboard.\n\tlist - Loads all keywords to clipboard.')

# Welcome user and explain usage
print("\tWelcome to the Extended Multiclipboard!\n")
print(usageInfo)

# Get and format user input
userInput = input('What would you like to do?\n').split()
userInput = [word.lower() for word in userInput]
numWords = len(userInput)

# Validate user input
if numWords != 1 or numWords != 2:
    print(usageInfo)

# User wants to save new content
elif numWords == 2 and userInput[0] == 'save':
    mcbShelf[userInput[1]] = pyperclip.paste()

# User wants a list of current keywords
elif numWords == 1 and userInput[0] == 'list':
    pyperclip.copy(str(list(mcbShelf.keys())))

# User wants to add new content
elif numWords == 1 and userInput[0] in mcbShelf:
    pyperclip.copy(mcbShelf[userInput[1]])

mcbShelf.close()
