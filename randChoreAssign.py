#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "Random Chore Assignment Emailer"
# from "Automate The Boring Stuff", by Al Sweigart,
# Chapter 16.
#
# "Write a program that takes a list of people’s email addresses
# and a list of chores that need to be done and randomly assigns
# chores to people. Email each person their assigned chores. If
# you’re feeling ambitious, keep a record of each person’s
# previously assigned chores so that you can make sure the program
# avoids assigning anyone the same chore they did last time. For
# another possible feature, schedule the program to run once a
# week automatically."
#
# CSV files requirements:
# * residents.csv: <resident name>,<resident email>
# * chores.csv: <chore>
#
# Nadia Borsch      misc@nborsch.com        Jun/2018

import csv
from getpass import getpass
import os
from random import choice
import re
import smtplib


def not_found():
    """Alert user that file was not found and quit program"""

    print("File not found, please try again.")
    quit()


def pick_chore(chores, residents, records):
    """Pick a random chore for each resident, considering
    the record of previously assigned chores"""

    assignments = []

    for resident, email in residents.items():

        # No record of previously assigned chores
        if not records:
            chore = choice(chores)
        else:
            # Make sure assigned chore is not a repeat of last time
            while True:
                chore = choice(chores)
                if chore != records[resident]:
                    break

        # Assign chore and remove it from chores list
        assignments.append([resident, email, chore])
        chores.remove(chore)

    # Returns dictionary of residents, their emails, and their assigned chores
    return assignments


def save_records(assignments):
    """Takes on a dictionary of residents and their assigned
    chores and saves the data into a csv file"""

    with open("records.csv", "w", newline="") as records:
        records_writer = csv.writer(records)

        for assignment in assignments:
            # Save name, email, and chore for current assignments
            records_writer.writerow([*assignment])


def validate_email(email):
    """Checks if an input is a properly formatted email address
    using regex and returns True or False"""

    # Create email validation regex
    regex = re.compile('''(
        [a-zA-Z0-9._%+-]+      # username
        @
        [a-zA-Z0-9.-]+         # domain name
        (\.[a-zA-Z]{2,4})      # top level domain name
    )''', re.VERBOSE)

    return bool(regex.search(email))


def mail_assignments(email, pwd, assignments):
    """Composes and emails assigned chore to corresponding resident"""

    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(email, pwd)

    for assignment in assignments:

        from_address = email
        to_name, to_address, chore = assignment
        body = (
            f"Subject: Your house chore\nHello, {to_name},\n\n"
            f"Your chore is:\n\n"
            f"{chore}.\n\n"
            f"Please make sure to complete it ASAP =)\n\n"
            f"Thank you and have a good one!"
            )

        print(f"Emailing {to_name} ({to_address})...")
        status = smtp.sendmail(from_address, to_address, body)

        if status != {}:
            print(f"There was a problem emailing {to_name}: {status}")

    smtp.quit()


def main():
    # Program presentation
    print(f"\n{'Random Chore Assignment Emailer':>40}")
    print(f"{'^^^^^^ ^^^^^ ^^^^^^^^^^ ^^^^^^^':>40}\n")

    # Get residents info csv file
    print(f"Current working directory is {os.getcwd()}.")

    while True:
        residents_file = input("Please enter the residents info csv file:\n")
        if residents_file.endswith(".csv"):
            break

    # Get chores csv file
    while True:
        chores_file = input(
            "\nPlease enter the chores csv file (one chore per line):\n"
            )
        if chores_file.endswith(".csv"):
            break

    # Load residents info csv file
    try:
        with open(residents_file) as residents_csv:
            residents_reader = csv.reader(residents_csv)

            # Retrieve residents info
            residents_info = {}
            for row in residents_reader:
                residents_info[row[0]] = row[1]

    except FileNotFoundError:
        not_found()

    # Load chores csv file
    try:
        with open(chores_file) as chores_csv:
            chores_reader = csv.reader(chores_csv)

            # Retrieve chores info
            chores_list = []
            for row in chores_reader:
                chores_list.append(row[0])

    except FileNotFoundError:
        not_found()

    # Load records of previously assigned chores
    try:
        with open("records.csv") as records_csv:
            records_reader = csv.reader(records_csv)

            # Retrieve records
            records_info = {}
            for row in records_reader:
                records_info[row[0]] = row[1]

    except FileNotFoundError:
        records_info = {}

    print("\nAssigning chores...")
    assigned_chores = pick_chore(chores_list, residents_info, records_info)

    print("Saving record of assigned chores...")
    save_records(assigned_chores)

    # Get email account username
    while True:
        email = input(
            "\nPlease enter the Gmail address from which to send "
            "assignment messages:\n"
            )
        if validate_email(email) is True:
            break

    # Get email account password
    while True:
        pwd = getpass(f"\nPlease enter the Gmail password for {email}:\n")
        if pwd:
            break

    mail_assignments(email, pwd, assigned_chores)

    print("\nAll done!")


if __name__ == '__main__':
    main()
