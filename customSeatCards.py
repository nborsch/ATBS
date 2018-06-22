#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "Custom Seating Cards" from "Automate The
# Boring Stuff", by Al Sweigart, Chapter 17.
#
# "Chapter 13 included a practice project to create custom invitations from a
# list of guests in a plaintext file. As an additional project, use the pillow
# module to create images for custom seating cards for your guests. For each
# of the guests listed in the guests.txt file from the resources at
# http://nostarch.com/automatestuff/, generate an image file with the guest
# name and some flowery decoration.
#
# To ensure that each seating card is the same size, add a black rectangle on
# the edges of the invitation image so that when the image is printed out,
# there will be a guideline for cutting. The PNG files that Pillow produces
# are set to 72 pixels per inch, so a 4×5-inch card would require a
# 288 × 360-pixel image."
#
# Nadia Borsch      misc@nborsch.com        Jun/2018

import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Constants
TEMPLATE = "template.jpg"
COLOR = "black"
TXT_FONT = ImageFont.truetype("georgia.ttf", 60)


def open_guestlist(guest_file):
    """
    Opens a plain text file and returns its lines. Takes in a string
    representing the name of the plain text file and returns a list
    of strings, one for each line in the file.
    """

    try:
        with open(guest_file) as guests:

            return guests.readlines()

    except FileNotFoundError:
        print("Guestlist file not found or corrupted, please try again.")


def process_guestlist(guest_file):
    """
    Processes a list of names to make individual seating cards. Takes in a
    list of strings representing guest names.
    """

    guests = open_guestlist(os.path.basename(guest_file))

    for guest in guests:

        # Removing new line from guest string
        guest = guest.strip()

        make_card(guest)


def make_card(guest):
    """
    Creates image files for individual seating cards. Takes in a string
    representing a guest name.
    """

    # Set up card variables
    try:
        card = Image.open(TEMPLATE).copy()
    except IOError:
        print("Template image file not found or corrupted, please try again.")
        quit()

    print(f"Creating seating card for {guest}...")

    card_width, card_height = card.size
    custom_guest = ImageDraw.Draw(card)
    custom_width, custom_height = custom_guest.textsize(guest, font=TXT_FONT)

    # Width and height for centering text
    center_width = (card_width - custom_width) / 2
    center_height = (card_height - custom_height) / 2

    # Drawing text
    custom_guest.text(
        (center_width, center_height),
        guest,
        fill=COLOR,
        font=TXT_FONT
        )

    # Drawing borders
    points = [
        (0, 0),
        (card_width - 3, 0),
        (card_width - 3, card_height - 3),
        (0, card_height - 3), (0, 0)
        ]

    custom_guest.line(points, fill=COLOR, width=3)

    # Create filename and save card image file
    filename = guest.lower().replace(" ", "").replace(".", "") + ".png"
    card.save(filename)


def main():
    # Program presentation
    print(f"\n{'Custom Seating Cards':>45}")
    print(f"{'###### ####### #####':>45}\n")
    print("Creates custom seating cards from a guest list.\n")

    while True:
        guest_file = input(
            "Please enter the full path for the guest list file (.txt only):\n"
            )
        if guest_file.endswith(".txt"):
            break
        else:
            print("Invalid file, please try again.")

    process_guestlist(guest_file)

    print("Done.")


if __name__ == '__main__':
    main()
