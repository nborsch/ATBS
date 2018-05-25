#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "Mad Libs"
# from "Automate The Boring Stuff", by Al Sweigart,
# Chapter 8.
#
# "Create a Mad Libs program that reads in text files and lets the user add 
# their own text anywhere the word ADJECTIVE, NOUN, ADVERB, or VERB appears 
# in the text file."
# 
# Nadia Borsch      misc@nborsch.com        May/2018

import re

# Open and read template file
madlibs = open('madlibs.txt', 'r')
template = madlibs.read()

print('{0:>30}'.format('MAD LIBS TIME!'))

# Set the lists to hold words
replaceables = [re.compile('ADJECTIVE'), re.compile('NOUN'), re.compile('VERB'), re.compile('NOUN')]
words = []
items = ['n adjective', ' noun', ' verb (past tense)', ' noun']

# Obtain and save user input
for word in items:
    words.append(input(f'Enter a{word}: ').lower())

# Replace words in string
for i in range(len(replaceables)):
    template = replaceables[i].sub(words[i], template, 1)

print(template)

madlibs.close()