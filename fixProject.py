#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "Extending and Fixing the Chapter Project
# Programs" from "Automate The Boring Stuff", by Al Sweigart, Chapter 17.
#
# "The resizeAndAddLogo.py program in this chapter works with PNG and JPEG
# files, but Pillow supports many more formats than just these two. Extend
# resizeAndAddLogo.py to process GIF and BMP images as well.
#
# Another small issue is that the program modifies PNG and JPEG files only if
# their file extensions are set in lowercase. For example, it will process
# zophie.png but not zophie.PNG. Change the code so that the file extension
# check is case insensitive.
#
# Finally, the logo added to the bottom-right corner is meant to be just a
# small mark, but if the image is about the same size as the logo itself, the
# result will look like Figure 17-16. Modify resizeAndAddLogo.py so that the
# image must be at least twice the width and height of the logo image before
# the logo is pasted. Otherwise, it should skip adding the logo."
#
# Nadia Borsch      misc@nborsch.com        Jun/2018

import os
from PIL import Image

# Constants
SQUARE_FIT_SIZE = 1000
LOGO_DEFAULT_SIZE = 300
file_ext = ["jpg", "jpeg", "png", "bmp", "gif"]


def apply_logo(img_folder, new_folder, logo_file):
    """
    Handles the application of a logo image onto an image. Takes in a string
    with a folder path for the images onto which the logo will be applied
    (img_folder), a string for the folder onto which to save the new images
    (new_folder), and the path for the logo image file (logo_file).
    """

    logo = handle_logo(logo_file)
    logo_width, logo_height = logo.size

    for filename in os.listdir("."):

        if not filename.endswith(tuple(file_ext)):
            # Skip files that are not images
            continue

        if filename == os.path.basename(logo_file):
            # Skip applying logo onto logo
            continue

        print(f"Opening file {filename}...")
        image = Image.open(filename)
        image_width, image_height = image.size

        if image_width < LOGO_DEFAULT_SIZE and image_height < \
                LOGO_DEFAULT_SIZE:
            # Skip files that are not at least twice the width and the height
            # of the logo
            print(f"{filename} is too small. Skipping...")
            continue

        if image_width > SQUARE_FIT_SIZE and image_height > SQUARE_FIT_SIZE:
            # Resize images larger than 1000px
            image = resize_img(image, SQUARE_FIT_SIZE)
            image_width, image_height = image.size

        # Apply logo
        print(f"Apllying logo onto {filename}...")
        image.paste(logo, (
            image_width - logo_width, image_height - logo_height), logo)

        # Save image with applied logo
        print(f"Saving {filename}...")
        image.save(os.path.join(new_folder, filename))


def handle_logo(logo_file):
    """
    Checks if a logo image needs to be resized to LOGO_DEFAULT_SIZE and
    resizes it if necessary. Takes in a string representing the logo image
    filename and returns an Image object of that logo image.
    """

    logo = Image.open(logo_file)
    logo_width, logo_height = logo.size

    # Check if logo is larger than 300px
    if logo_width > LOGO_DEFAULT_SIZE and logo_height > LOGO_DEFAULT_SIZE:
        logo = resize_img(logo, LOGO_DEFAULT_SIZE)

    return logo


def resize_img(img, size):
    """
    Resizes an image (img) according to the provided size. Takes in an Image
    object (img) and an int (size), and returns the resized Image object.
    """

    img_width, img_height = img.size

    # Logo is larger than 300px and width is larger than height
    if img_width > img_height:
        img_height = int((size / img_width) * img_height)
        img_width = size

    # Logo is larger than 300px and height is larger than width
    else:
        img_width = int((size / img_height) * img_width)
        img_height = size

    img = img.resize((img_width, img_height))

    return img


def main():
    # Program presentation
    print(f"\n{'Fixed Resize and Add Logo':>50}")
    print(f"{'^^^^^ ^^^^^^ ^^^ ^^^ ^^^^':>50}\n")
    print(f"Current working directory is {os.getcwd()}.")

    # Obtain photos folder path
    while True:
        img_folder = input(
            "Please enter the full path for the photos folder, or press ENTER "
            "to use the current folder:\n")

        if img_folder:
            os.chdir(img_folder)
            break
        else:
            img_folder = os.getcwd
            break

    print(f"Folder path {os.getcwd()} will be used.\n")

    # Obtain logo file and folder path
    while True:
        logo_file = input(
            "Please enter the logo filename (include full path if it's "
            "in a folder other than the current working directory):\n")
        if logo_file.lower().endswith(tuple(file_ext)):
            break
        else:
            print("Invalid path or file format. Please try again.")

    print(
        f"File '{os.path.basename(logo_file)}' will be used. It will be "
        "resized to 300px.")

    # Create new directory to store new files
    new_folder = os.path.join(os.getcwd(), "With Logo")
    os.makedirs(new_folder, exist_ok=True)

    apply_logo(img_folder, new_folder, logo_file)

    print("Done.")


if __name__ == '__main__':
    main()
