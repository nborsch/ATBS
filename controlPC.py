#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "Controlling Your Computer Through Email"
# from "Automate The Boring Stuff", by Al Sweigart,
# Chapter 16.
#
# "Write a program that checks an email account every 15 minutes for any
# instructions you email it and executes those instructions automatically.
# For example, BitTorrent is a peer-to-peer downloading system. Using free
# BitTorrent software such as qBittorrent, you can download large media files
# on your home computer. If you email the program a (completely legal, not at
# all piratical) BitTorrent link, the program will eventually check its email,
# find this message, extract the link, and then launch qBittorrent to start
# downloading the file."
#
# Nadia Borsch      misc@nborsch.com        Jun/2018

from getpass import getpass
import re
from subprocess import Popen
from threading import Thread
import time
from bs4 import BeautifulSoup
import imaplib
import imapclient
import pyzmail

# TODO
# ! Text after successful command execution
# ! Logging

# Constants
TORRENT = "C:\\Program Files\\qBittorrent\\qbittorrent.exe"


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


def check_email(username, password, key, email):
    """
    """

    # Log user in
    imap_client = login_imap(username, password)

    # Bypass size limit
    imaplib._MAXLINE = 10000000

    imap_client.select_folder("INBOX")

    if username.endswith("@gmail.com"):
        new_mail = imap_client.gmail_search(f"{key} from:{email}")
    else:
        new_mail = imap_client.search(["TEXT", key, "FROM", email])

    if new_mail:
        return imap_client, new_mail


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

    imap_client = imapclient.IMAPClient(find_imap(username), ssl=True)

    try:
        imap_client.login(username, pwd)
    except imaplib.IMAP4.error:
        print(f"Invalid username and/or password. Please try again.")
        quit()

    return imap_client


def process_msgs(messages):
    """
    """

    msgs_html = get_msgs(get_raw_msgs(messages))

    magnets = find_magnets(msgs_html)

    handle_magnets(magnets)

    # TODO find and execute commands

    # Delete emails after execution
    #delete_msgs(messages)

    # Log out of account
    messages[0].logout()


def get_raw_msgs(messages):
    """
    """

    imap_client, UIDs = messages
    fetched_msgs = imap_client.fetch(UIDs, ['BODY[]'])

    return fetched_msgs


def get_msgs(raw_msgs):
    """
    """

    ready_msgs = []

    for raw_msg in raw_msgs:
        message = pyzmail.PyzMessage.factory(raw_msgs[raw_msg][b'BODY[]'])
        message = message.html_part.get_payload().decode(
            message.html_part.charset)

        ready_msgs.append(message)

    return ready_msgs


def delete_msgs(messages):
    """
    """

    imap_client, UIDs = messages

    imap_client.delete_messages(UIDs)
    try:
        imapclient.expunge()
    except AttributeError:
        pass


def find_magnets(msgs_html):
    """
    """

    for html in msgs_html:
        soup = BeautifulSoup(html, "lxml")

        divs = soup.select("div")

        for div in divs:
            if div.getText().startswith("magnet:"):
                yield div.getText()


def handle_magnets(magnets):
    """
    """

    for magnet in magnets:
        launch_threads(magnet)


def launch_threads(magnet):
    """
    """

    thread = Thread(target=worker, args=(magnet,))
    thread.start()

def worker(magnet):
    """
    """

    open_magnet(magnet)


def open_magnet(magnet):
    """
    """

    process = Popen([TORRENT, magnet])

    while True:
        if process.poll() != None:
            send_txt(magnet)
            break
        
        time.sleep(10)


def send_txt(magnet):
    """
    """

    txt = magnet.split("=")[2]
    print(raw_txt)


def main():
    # Program presentation
    print(f"\n{'Controlling Your Computer Through Email':>70}")
    print(f"{'*********** **** ******** ******* *****':>70}\n")
    print(
        "Your email account (Gmail, Hotmail, or Yahoo) will be checked "
        " every 15 minutes for commands.\nA key will be required with "
        "every message to confirm identity.\n")

    # Get user email account
    while True:
        username = input("Please enter the email account to be checked:\n")
        if validate_email(username):
            break

    # Get user email account password
    while True:
        pwd = getpass(
            "\nPlease enter the password for the account to be checked:\n")
        if pwd:
            break

    # Get verification key
    while True:
        key = input("\nPlease enter the verification key:\n")
        if key:
            print(f"Key '{key}' will be used.\n")
            break

    # Get sender email account
    while True:
        email = input("Please enter the sender email address:\n")
        if validate_email(email):
            print(f"Sender '{email}' will be used.\n")
            break

    # Start program at user's command
    print("Press ENTER to start program. Press CTRL+C to exit.")
    input()
    print("Program started.")

    try:
        while True:
            new_mail = check_email(username, pwd, key, email)

            if new_mail:
                process_msgs(new_mail)

            # Wait 15 minutes to check again
            time.sleep(60 * 15)

    except KeyboardInterrupt:
        print("Program stopped. Quitting...")

        quit()

if __name__ == "__main__":
    main()
