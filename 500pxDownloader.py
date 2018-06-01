#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "Image Site Downloader"
# from "Automate The Boring Stuff", by Al Sweigart,
# Chapter 11.
#
# "Write a program that goes to a photo-sharing site like 
# Flickr or Imgur, searches for a category of photos, and 
# then downloads all the resulting images."
# 
# Nadia Borsch      misc@nborsch.com        May/2018

import bs4, requests, os
from selenium import webdriver
from time import sleep

print("")
print("{:>40}".format("500PX IMAGE DOWNLOADER"))
print("{:>40}".format("===== ===== =========="))

# Obtain search terms, create storage folder, set base URL
search_terms = input("Please enter the search terms for the images you'd like to download.\n")
print(f"\nSearch terms are: '{search_terms}'.\nImages will be saved to '{os.getcwd()}\{search_terms}'.")

# Define browser, search URL, and soup
browser = webdriver.Chrome()
browser.get(f"https://500px.com/search?submit=Submit+Query&q={search_terms}")
html = browser.page_source
soup = bs4.BeautifulSoup(html, "lxml")

# Find number of results
results = soup.select(".results-count")
results = results[0].getText()
results = results.split()
results = results[0]

# Quit program if no results are found
if results == 0:
    print("\nYour search returned no results. Please try again.")
    quit()
else:
    # Create storage folder based on search terms
    os.makedirs(f"{search_terms}", exist_ok=True)
    os.chdir(search_terms)

# Create list of images
img_list = soup.select(".photo_link")

# Download images
for i in range(len(img_list)):
    try:
        # Find individual photo's gallery URL
        gallery = 'http://500px.com' + img_list[i].get('href')
        browser.get(gallery)

        # Find individual photo's URL and title
        photo = browser.find_element_by_css_selector(".photo")
        photo_url = photo.get_attribute("src")
        photo_name = photo.get_attribute("alt")
        
        res = requests.get(photo_url)
        res.raise_for_status()
    except requests.exceptions.MissingSchema:
        # If an error occurs, skip to next photo
        continue

    # Save photo
    print(f"Saving {photo_name}.jpg...")
    photo_file = open(f"{photo_name}.jpg", "wb")
    for part in res.iter_content(100000):
        photo_file.write(part)
    photo_file.close()

print("Done.")
