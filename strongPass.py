#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "Strong Password Detection"
# from "Automate The Boring Stuff", by Al Sweigart,
# Chapter 7.
# 
# Nadia Borsch      misc@nborsch.com        May/2018

import re

print('Welcome to the Strong Password Detection Program!')

password = input('Please enter the password you want to check.\n\n')

upperLower = re.compile(r'[A-Z]+[a-z]+')

digit = re.compile(r'[0-9]+')

# TODO: check if password is at least 8 characters long

if len(password) < 8:
    print('\nYour password is too short.')

# TODO: check if password contains both uppercase and lowercase characters

elif upperLower.search(password) == None:
    print('\nA strong password must have both uppercase and lowercase characters.')

# TODO check if password has at least one digit

elif digit.search(password) == None:
    print('\nA strong password must have at least one digit.')

else:
    print('\nAll good!')