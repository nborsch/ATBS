#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "Regex Version of strip()"
# from "Automate The Boring Stuff", by Al Sweigart,
# Chapter 7.
# 
# Nadia Borsch      misc@nborsch.com        May/2018

import re

def regexStrip(s, chars):
    if not chars:
        left = re.compile(r'^\s*')
        right = re.compile(r'\s*$')

        s = left.sub('', s)
        s = right.sub('', s)
        
    else:
        left = re.compile(r'^[' + re.escape(chars) + r']*')
        right = re.compile(r'[' + re.escape(chars) + r']*$')
        
        s = left.sub('', s)
        s = right.sub('', s)
    
    return s

# Start program and obtain user input
print('Regex Version of strip()')
user_string = input('Please enter the string you want to strip.\n')
stripper = input('Please enter the string you want to use to do the stripping or leave it blank to strip all whitespaces.\n')

print(regexStrip(user_string, stripper))