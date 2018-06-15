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
    Works with Gmail, Hotmail, and Yahoo ('.com' addresses only.)
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
    # From this year backwards until Hotmail launch
    years = [i for i in range(datetime.now().year, 1995, -1)]

    for year in years:
        # Retrieve messages for a one-year period at a time
        since = datetime(year - 1, 12, 31).strftime('%d-%b-%Y')
        before = datetime(year, 12, 31).strftime('%d-%b-%Y')
        batch = imap_client.search([
            "TEXT", "unsubscribe",
            "SINCE", since,
            "BEFORE", before
            ])
        if batch:
            yield batch


def raw_msgs(imap_client):
    """
    Processes email messages by UID and returns the raw message body.
    """

    return imap_client.fetch(list(email_search(imap_client))[0], ['BODY[]'])


def msg_body(imap_client):
    """
    Processes raw message bodies into HTML.
    Returns the sender and the HTML body.
    """
    raw = raw_msgs(imap_client)

    for UID in raw:
        message = pyzmail.PyzMessage.factory(raw[UID][b'BODY[]'])
        sender = message.get_address("from")

        if len(sender) > 1:
            sender = sender[1]
        else:
            sender = sender[2]

        message = message.html_part.get_payload().decode(
            message.html_part.charset)

        yield sender, message


def check_senders(imap_client):
    """
    Checks if there are duplicate senders in message list.
    Returns only messages with unique senders.
    """

    messages = list(msg_body(imap_client))
    senders = []

    for message in messages:
        sender = message[0]

        if sender not in senders:
            senders.append(sender)
            yield message[1]


def unsub_links(imap_client):
    """
    Takes in an HTML message body and parses it for
    'unsubscribe' links and returns such links if found
    """

    bodies = list(check_senders(imap_client))

    regex = re.compile(".*(unsubscribe).*", re.I)

    print("Finding 'unsubscribe' links...")
    for body in bodies:
        # Parse each message for links
        soup = BeautifulSoup(body, "lxml")
        link_elems = soup.select("a")

        # Parse each link for the word "unsubscribe"
        # If found, add to links list
        for link_elem in link_elems:
            if regex.search(link_elem.getText()):
                    yield link_elem.get("href")


def open_link(link):
    """
    Takes in a link and opens it in a browser tab
    """

    print("Opening link in browser...")
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
