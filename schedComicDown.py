#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "Scheduled Web Comic Downloader"
# from "Automate The Boring Stuff", by Al Sweigart,
# Chapter 15.
#
# "Write a program that checks the websites of several 
# web comics and automatically downloads the images if 
# the comic was updated since the program’s last visit. 
# Your operating system’s scheduler (Scheduled Tasks 
# on Windows, launchd on OS X, and cron on Linux) 
# can run your Python program once a day. The Python 
# program itself can download the comic and then copy 
# it to your desktop so that it is easy to find. This will 
# free you from having to check the website yourself 
# to see whether it has updated. "
# 
# Nadia Borsch      misc@nborsch.com        Jun/2018

import csv
import os
import threading
import time
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import datetime
import requests

def downloader(title, base_url, element, current_visit_data, saved_filename=None):
    """Downloads latest web comics"""
    res = requests.get(base_url)
    res.raise_for_status()

    # Find current comic image URL
    soup = BeautifulSoup(res.text, "lxml")
    comic_elem = soup.select(element)

    if comic_elem == []:
        # Skip comic, not found
        print(f"Could not find current comic for {title}.")
        return None
    else:
        comic_url = comic_elem[0].get("src")
        comic_filename = os.path.basename(comic_url)

        # Check current comic file against saved file
        if saved_filename and comic_filename.lower() == saved_filename.lower():
            # No updates have been found
            print(f"No updates for {title}.")
            return None
        else:
            # Get and save comic
            print(f"Downloading latest comic from {title}...")

            if not urlparse(comic_url).netloc:
                # URL for comic image is relative
                comic_url = f"{base_url}/{comic_url}"

            res = requests.get(comic_url)
            res.raise_for_status()

            # Create folder on desktop to save all files
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            folder = f"C:{os.path.join(os.environ['HOMEPATH'], 'Desktop')}\\{current_date} Web Comics"
            os.makedirs(folder, exist_ok=True)

            with open(f"{folder}\{comic_filename}", "wb") as comic_file:
                for part in res.iter_content(100000):
                    comic_file.write(part)

            # Log filename
            current_visit_data[title] = comic_filename

def main():
    # Program presentation
    print(f"\n{'Scheduled Web Comic Downloader':>42}")
    print(f"{'********* *** ***** **********':>42}\n")
    print("The following web comics will be checked for updates:\n\n"
            ":: Left-handed Toons\t\t"
            ":: Buttersafe\n"
            ":: Two Guys and Guy\t\t"
            ":: Savage Chickens\n"
            ":: Channelate\t\t\t"
            ":: Extra Ordinary\n"
            ":: Wonderella\t\t\t"
            ":: Moonbeard\n"
            ":: Happle Tea\t\t\t"
            ":: Saturday Morning Breakfast Cereal\n"),
    print("Comics will be saved on your Desktop under 'Updated Web Comics'.\n")

    # Open CSV file that stores last visit's dates
    try:
        with open("schedComicDown.csv") as last_visit_file:
            last_visit_reader = csv.reader(last_visit_file)

            # Retrieve last visit data from file
            last_visit_data = {}
            for row in last_visit_reader:
                last_visit_data[row[0]] = row[1]

    except FileNotFoundError:
        last_visit_data = {}

    # Data structure for the comics updated info
    current_visit_data = {"Last Checked:": time.time()}

    # Comics to check and their parameters
    comics = [
        ["Left-handed Toons", "http://www.lefthandedtoons.com/", ".comicimage"],
        ["Buttersafe", "http://buttersafe.com/", "#comic img"],
        ["Two Guys and Guy", "http://www.twogag.com/", "div#comic div a img"],
        ["Savage Chickens", "http://www.savagechickens.com/", "div.entry_content p img"],
        ["Channelate", "http://www.channelate.com/", "div#comic img"],
        ["Extra Ordinary", "http://www.exocomics.com/", "a.comic img"],
        ["Wonderella", "http://nonadventures.com/", "div#comic img"],
        ["Moonbeard", "http://moonbeard.com/", "div#comic div a img"],
        ["Happle Tea", "http://www.happletea.com/", "div#comic img"],
        ["Saturday Morning Breakfast Cereal", "https://www.smbc-comics.com/", "img#cc-comic"],
    ]

    # Create and start thread objects
    downloads = []
    for comic in comics:
        comic.append(current_visit_data)
        if comic[0] in last_visit_data.keys():
            # Comic has been checked before, send saved filename as argument
            comic.append(last_visit_data[comic[0]])

        download = threading.Thread(target=downloader, args=comic)
        downloads.append(download)
        download.start()

    # Wait for all threads to end
    for download in downloads:
        download.join()

    # Add current comic updates to csv file
    updated_data = {**last_visit_data, **current_visit_data}

    # Save current date on file
    with open("schedComicDown.csv", "w", newline="") as current_visit_file:
        current_visit_writer = csv.writer(current_visit_file)

        for key, value in updated_data.items():
            current_visit_writer.writerow([key, value])

    print("All done!")

if __name__ == '__main__':
    main()
