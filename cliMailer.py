#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "Command Line Emailer"
# from "Automate The Boring Stuff", by Al Sweigart,
# Chapter 11.
#
# "Write a program that takes an email address and string 
# of text on the command line and then, using Selenium, logs 
# into your email account and sends an email of the string to 
# the provided address."
#
# Usage: <email address> <message>
# 
# Nadia Borsch      misc@nborsch.com        May/2018

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import sys

# DRY for finding elements
def elems(type_elem, string_elem):
    if type_elem == "selector":
        return browser.find_element_by_css_selector(string_elem)
    elif type_elem == "class":
        return browser.find_element_by_class_name(string_elem)

# Validate user input
if len(sys.argv) < 3:
    print("Usage: <email address> <message>")
    quit()

# Define browser, initial URL, and inputs
browser = webdriver.Chrome()
browser.get("https://gmail.com")
email_address = sys.argv[1]
email_message = ' '.join(sys.argv[2:])

try:
    # Click "Sign In" button
    elems("class", "gmail-nav__nav-link__sign-in").click()

    # Fill in and submit username field
    username = elems("class", "whsOnd")
    username.send_keys("ENTER USERNAME HERE")
    elems("selector", "#identifierNext > content > span").click()
    sleep(2)

    # Fill in and submit password field
    pwd = elems("class", "whsOnd")
    pwd.send_keys("ENTER PASSWORD HERE")
    elems("selector", "#passwordNext > content > span").click()
    sleep(2)

    # Click compose button
    elems("class", "T-I-KE").click()
    sleep(2)

    # Fill in recipient field
    recipient = elems("class", "vO")
    recipient.send_keys(email_address)
    recipient.send_keys(Keys.TAB)
    sleep(2)

    # Fill in subject field
    subject = elems("class", "aoT")
    subject.send_keys("Automated message")

    # Fill in message body
    body = elems("class", "editable")
    body.send_keys(email_message)

    # Click "Send" button
    elems("class", "aoO").click()

except Exception as err:
    print(f"Could not finish process: {err}")