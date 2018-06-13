#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "Auto Unsubscriber"
# from "Automate The Boring Stuff", by Al Sweigart,
# Chapter 16.
#
# "Write a program that scans through your email account, finds all the
# unsubscribe links in all your emails, and automatically opens them in a
# browser. This program will have to log in to your email provider’s IMAP
# server and download all of your emails. You can use BeautifulSoup
# (covered in Chapter 11) to check for any instance where the word
# 'unsubscribe' occurs within an HTML link tag.
#
# Once you have a list of these URLs, you can use webbrowser.open() to
# automatically open all of these links in a browser.
#
# You’ll still have to manually go through and complete any additional
# steps to unsubscribe yourself from these lists."
#
# Nadia Borsch      misc@nborsch.com        Jun/2018

from getpass import getpass
import imaplib
import webbrowser
import re
from bs4 import BeautifulSoup
import imapclient
import pyzmail

# TODO
# Pass IMAP functions to each other
# Open URLs in browser using webbrowser.open()


def validate_email(email):
    """Validates a string for properly formatted
    email address and returns True or False"""

    regex = re.compile(
        r'''[a-zA-Z0-9._%+-]+   # username
        @
        [a-zA-Z0-9.-]+          # domain name
        (\.[a-zA-Z]{2,4})       # top level domain name
        ''', re.VERBOSE
        )

    return bool(regex.search(email))


def find_imap(email):
    """Figures out and returns the IMAP client according to email address.
    Works with Gmail, Hotmail, and Yahoo ('.com' addresses only)"""

    provider = email.split("@")[1]

    if provider == "gmail.com":
        return "imap.gmail.com"
    elif provider == "hotmail.com":
        return "imap-mail.outlook.com"
    elif provider == "yahoo.com":
        return "imap.mail.yahoo.com"


def login_imap(username, pwd):
    """Logs 'username' into 'imap' client and returns IMAPClient object."""

    print("Logging into email account...")
    imap_client = imapclient.IMAPClient(find_imap(username), ssl=True)

    try:
        imap_client.login(username, pwd)
    except imaplib.IMAP4.error:
        print(f"Invalid username and/or password. Please try again.")
        quit()

    return imap_client


def email_search(imap_client):
    """Returns a list with the UIDs of all email messages in the user's
    inbox."""

    # Bypass size limit
    imaplib._MAXLINE = 10000000

    print("Retrieving messages...")
    imap_client.select_folder("INBOX", readonly=True)
    UIDs = imap_client.search(["ALL"])

    return UIDs


def find_msgs(UIDs, imap_client):
    """Searches through each message in the user's inbox for
    'unsubscribe' links and returns a list of such links"""

    raw_msgs = imap_client.fetch(UIDs, ['BODY[]'])

    messages = []

    for UID in raw_msgs:
        message = pyzmail.PyzMessage.factory(raw_msgs[UID][b'BODY[]'])
        message = message.html_part.get_payload().decode(
            message.html_part.charset)

        messages.append(message)

    return messages


def find_unsub_links(messages):
    """Takes in a list of HTML message bodies and parses them for
    'unsubscribe' links"""

    regex = re.compile(".*(unsubscribe|Unsubscribe|UNSUBSCRIBE).*")
    unsub_links = []

    print("Finding 'unsubscribe' links...")
    for message in messages:
        # Parse each message for links
        soup = BeautifulSoup(message, "lxml")
        link_elems = soup.select("a")

        # Parse each link for the word "unsubscribe"
        # If found, add to links list
        for link_elem in link_elems:
            if regex.search(link_elem.getText()):
                unsub_links.append(link_elem.get("href"))

    return unsub_links


def open_links(links):
    """Takes in a list of links and opens them in the browser."""

    print("Opening links in browser...\n")
    for link in links:
        webbrowser.open(link)


def main():
    # Program presentation
    print(f"\n{'Auto Unsubscriber':>25}")
    print(f"{'++++ ++++++++++++':>25}\n")

    # Get user email account username and address
    while True:
        username = input("Please enter your email address:\n")
        if validate_email(username):
            break

    # Get user email account password
    while True:
        pwd = getpass("\nPlease enter your password:\n")
        if pwd:
            break

    # Log user in and retrieve UIDs for all messages
    imap_client = login_imap(username, pwd)
    UIDs = email_search(imap_client)

    # Retrieve all links and parse for 'unsubscribe' links
    links = find_unsub_links(find_msgs(UIDs, imap_client))
    open_links(links)

    # Disconnect from IMAP server
    imap_client.logout()

    print("Done.")


if __name__ == '__main__':
    main()
