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
import logging
import re
import subprocess
import time
from bs4 import BeautifulSoup
import imaplib
import imapclient
from twilio.rest import Client
import pyzmail

# Constants
TORRENT = "C:\\Program Files\\qBittorrent\\qbittorrent.exe"
SMS_TO = ""
SMS_FROM = ""
TWILIO_ACCT = ""
TWILIO_TOKEN = ""

# Logging configuration
logging.basicConfig(
    filename="controlPC.log",
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s \n')


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
    Checks an email account for new messages that match the criteria for a
    torrent download. Returns a tuple with the IMAPClient object and a list
    of UIDs of the matching messages.
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

    logging.info("Email account successfully checked.")

    if new_mail:
        logging.info("Email command found.")
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
        logging.info("Email account login successful.")

    except (imaplib.IMAP4.error, UnicodeEncodeError):
        print(f"Invalid username and/or password. Please try again.")
        logging.info("Email account login unsuccessful.")

        quit()

    return imap_client


def process_msgs(messages):
    """
    Handles processing of messages for extraction of magnets, messages
    deletion, and logging out of IMAP server. Takes a tuple of an IMAPClient
    object and a list of UIDs, and returns a generator object for the
    extracted magnet links.
    """

    logging.info("Starting processing of email command(s).")

    msgs_html = get_msgs(get_raw_msgs(messages))

    magnets = find_magnets(msgs_html)

    # Delete emails after execution
    delete_msgs(messages)

    # Log out of account
    messages[0].logout()

    return magnets


def get_raw_msgs(messages):
    """
    Fetches the raw body of email messages from an IMAP server. Takes in a
    tuple with the IMAPClient object and a list of UIDs. Returns a list with
    the raw body of all fetched messages.
    """

    imap_client, UIDs = messages
    fetched_msgs = imap_client.fetch(UIDs, ['BODY[]'])

    return fetched_msgs


def get_msgs(raw_msgs):
    """
    Processes raw message body into HTML message body. Takes in a list with
    raw message bodies and returns a generator object of HTML message bodies.
    """

    for raw_msg in raw_msgs:
        message = pyzmail.PyzMessage.factory(raw_msgs[raw_msg][b'BODY[]'])
        message = message.html_part.get_payload().decode(
            message.html_part.charset)

        yield message


def delete_msgs(messages):
    """
    Deletes email messages from an IMAP server. Takes in a tuple with the
    IMAPClient object and a list of UIDs.
    """

    imap_client, UIDs = messages

    imap_client.delete_messages(UIDs)
    try:
        imapclient.expunge()
    except AttributeError:
        # For some IMAP servers, expunge() isn't necessary
        pass


def find_magnets(msgs_html):
    """
    Extracts torrent magnet links from HTML message bodies using regex. Takes
    in a generator object of HTML message bodies and return a generator object
    of complete magnet links.
    """

    regex = re.compile(r"(magnet:\?xt=urn:btih:\S+)(&amp;dn=|&dn=)([^<\s]*)?")

    for msg_html in msgs_html:
        soup = BeautifulSoup(msg_html, "lxml")
        divs = soup.select("div")

        for div in divs:
            if regex.search(div.getText()):
                # The text in the <div> element matches the pattern of
                # a magnetic link
                magnet = regex.search(div.getText()).group()
                logging.info("Magnet link found and extracted.")

                yield magnet


def open_magnet(magnet):
    """
    Opens qBittorrent with a magnetic link. Takes in a string of a magnetic
    link.
    """

    subprocess.Popen([TORRENT, magnet])

    send_txt(magnet)


def send_txt(magnet):
    """
    Sends a text message containing the name of the file in a magnetic link.
    Takes in a string with a magnetic link.
    """

    filename = magnet.split("=")[2]
    if "+" in filename:
        filename.replace("+", " ")

    account = TWILIO_ACCT
    token = TWILIO_TOKEN
    sms_client = Client(account, token)
    sms_body = f"The file {filename} has started downloading."

    sms_client.messages.create(
        to=SMS_TO,
        from_=SMS_FROM,
        body=sms_body
    )

    logging.info(f"SMS for thread {magnet} sent.")


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
    logging.info("Program started.")

    try:
        while True:
            logging.info("New program cycle.")
            new_mail = check_email(username, pwd, key, email)

            if new_mail:
                magnets = process_msgs(new_mail)

                for magnet in magnets:
                    open_magnet(magnet)

            # Wait 15 minutes to check again
            time.sleep(60 * 15)

    except KeyboardInterrupt:
        print("Program stopped. Quitting...")
        logging.info("Program stopped.")

        quit()


if __name__ == "__main__":
    main()
