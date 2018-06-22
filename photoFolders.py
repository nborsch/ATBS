#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "Identifying Photo Folders on the Hard Drive"
# from "Automate The Boring Stuff", by Al Sweigart, Chapter 17.
#
# "Write a program that goes through every folder on your hard drive and finds
# potential photo folders. Of course, first you’ll have to define what you
# consider a “photo folder” to be; let’s say that it’s any folder where more
# than half of the files are photos. And how do you define what files are
# photos?
#
# First, a photo file must have the file extension .png or .jpg. Also, photos
# are large images; a photo file’s width and height must both be larger than
# 500 pixels. This is a safe bet, since most digital camera photos are several
# thousand pixels in width and height.
#
# When the program runs, it should print the absolute path of any photo
# folders to the screen."
#
# Nadia Borsch      misc@nborsch.com        Jun/2018

import os
from PIL import Image

# Constants
MIN_PHOTO_SIZE = 500


def scan_hdd(hdd):
    """
    Walks a directory tree and identifies folders for which more than half of
    the total files are image files (png or jpg) larger than 500px, and prints
    the fodler path onto stdout if so. Takes in a string representing an HDD
    letter.
    """

    for foldername, subfolders, filenames in os.walk(hdd):

        photo_files = 0
        other_files = 0

        # Check files in current folder
        for filename in filenames:
            if not filename.lower().endswith(("jpg", "jpeg", "png")):
                # File is not a photo file
                other_files += 1
                continue

            try:
                img = Image.open(filename)
            except FileNotFoundError:
                # Filename is invalid
                continue

            img_width, img_height = img.size

            if img_width < MIN_PHOTO_SIZE and img_height < MIN_PHOTO_SIZE:
                # File is not large enough to be considered a photo
                other_files += 1
                continue

            photo_files += 1

        if photo_files > (photo_files + other_files) / 2:
            print(foldername)


def main():
    # Program presentation
    print(f"\n{'Photo Folder Finder':>55}")
    print(f"{'***** ****** ******':>55}\n")
    print(
        "This program will help you identify the photo folders in your hard "
        "drive. A folder is considered\na photo folder if more than half of "
        "its files are photos, and a file is considered a photo if:\n\n\t+ "
        "Its extension is either '.png' or '.jpg'\n\t+ The image width and "
        "height are larger than 500 pixels.\n\nFound photo folders will be "
        "displayed on the screen.\n")

    # Obtain the letter for the HDD to be scanned
    while True:
        hdd = input(
            "Please enter the letter for the hard drive you'd like to "
            "have scanned, or press ENTER to use 'C:\\'.\n")

        if hdd.endswith(":\\"):
            break
        elif hdd.endswith(":"):
            hdd = hdd + "\\"
            break
        elif hdd:
            hdd = hdd + ":\\"
            break
        else:
            hdd = "C:\\"
            break

    # Wait for user input to start
    try:
        while True:
            input("Press ENTER to start the scan.\n")

            scan_hdd(hdd)

            print("\nScan finished.")
            break

    # Quit on user command
    except KeyboardInterrupt:
        print("Program stopped. Quitting...")
        quit()


if __name__ == '__main__':
    main()
