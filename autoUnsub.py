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

from datetime import datetime
from getpass import getpass
import imaplib
import webbrowser
import re
from bs4 import BeautifulSoup
import imapclient
import pyzmail


def validate_email(email):
    """
    Validates a string for properly formatted
    email address and returns True or False
    """

    regex = re.compile(
        r'''[a-zA-Z0-9._%+-]+   # username
        @
        [a-zA-Z0-9.-]+          # domain name
        (\.[a-zA-Z]{2,4})       # top level domain name
        ''', re.VERBOSE
        )

    return bool(regex.search(email))


def find_imap(email):
    """
    Figures out and returns the IMAP client according to email address.
    Works with Gmail, Hotmail, and Yahoo ('.com' addresses only)
    """

    provider = email.split("@")[1]

    if provider == "gmail.com":
        return "imap.gmail.com"
    elif provider == "hotmail.com":
        return "imap-mail.outlook.com"
    elif provider == "yahoo.com":
        return "imap.mail.yahoo.com"


def login_imap(username, pwd):
    """
    Logs 'username' into 'imap' client and returns IMAPClient object.
    """

    print("Logging into email account...")
    imap_client = imapclient.IMAPClient(find_imap(username), ssl=True)

    try:
        imap_client.login(username, pwd)
    except imaplib.IMAP4.error:
        print(f"Invalid username and/or password. Please try again.")
        quit()

    return imap_client


def email_search(imap_client):
    """
    Searches user's inbox and returns the UID of all the email messages
    that have the word "unsubscribe" (case insensitive) somewhere in the body.
    """

    # Bypass size limit
    imaplib._MAXLINE = 10000000

    print("Retrieving messages...")
    imap_client.select_folder("INBOX", readonly=True)
    months = [i for i in range(1, 13)]
    # Years to date since Hotmail launch
    years = [i for i in range(2017, datetime.now().year + 1)]

    UIDs = []

    for year in years:
        for month in months:
            since = datetime(year, month, 1).strftime('%d-%b-%Y')
            before = datetime(year, month % 12 + 1, 1).strftime('%d-%b-%Y')
            batch = imap_client.search([
                "TEXT", "unsubscribe",
                "SINCE", since,
                "BEFORE", before
                ])
            if batch:
                UIDs += batch

    return UIDs


def raw_msgs(imap_client):
    """
    Processes an UID to return the raw message body
    """

    UIDs = email_search(imap_client)

    return imap_client.fetch(UIDs, ['BODY[]'])


def msg_body(imap_client):
    """
    """

    raw = raw_msgs(imap_client)

    for UID in raw:
        message = pyzmail.PyzMessage.factory(raw[UID][b'BODY[]'])
        message = message.html_part.get_payload().decode(
            message.html_part.charset)

        yield message


def unsub_links(imap_client):
    """
    Takes in an HTML message body and parses it for
    'unsubscribe' links and returns such links if found
    """

    messages = list(msg_body(imap_client))

    regex = re.compile(".*(unsubscribe).*", re.I)
    links = []

    print("Finding 'unsubscribe' links...")
    for message in messages:
        # Parse each message for links
        soup = BeautifulSoup(message, "lxml")
        link_elems = soup.select("a")

        # Parse each link for the word "unsubscribe"
        # If found, add to links list
        for link_elem in link_elems:
            if regex.search(link_elem.getText()):
                    links.append(link_elem.get("href"))

    return links


def open_link(link):
    """
    Takes in a link and opens it in a browser tab
    """

    print("Opening links in browser...\n")
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

    # Log user in
    imap_client = login_imap(username, pwd)

    # Get all links
    links = unsub_links(imap_client)

    # Retrieve all links and opens them in browser
    for link in links:
        open_link(link)

    # Disconnect from IMAP server
    imap_client.logout()

    print("Done.")


if __name__ == '__main__':
    main()
