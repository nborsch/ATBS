#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "2048" from "Automate The 
# Boring Stuff", by Al Sweigart, Chapter 11.
#
# "2048 is a simple game where you combine tiles by sliding 
# them up, down, left, or right with the arrow keys. You can 
# actually get a fairly high score by repeatedly sliding in 
# an up, right, down, and left pattern over and over again. 
# Write a program that will open the game at 
# https://gabrielecirulli.github.io/2048/ and keep sending 
# up, right, down, and left keystrokes to automatically 
# play the game."
# 
# Nadia Borsch      misc@nborsch.com        May/2018

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep

actions = {"up": Keys.UP, "right": Keys.RIGHT, "down": Keys.DOWN, "left": Keys.LEFT}

def play(key):
    if key in actions:
        game.send_keys(actions.get(key))
        sleep(0.05)
    
    return None

browser = webdriver.Chrome()
browser.get("https://gabrielecirulli.github.io/2048/")
sleep(0.5)
game = browser.find_element_by_tag_name("body")

while True:
    play("up")
    play("right")
    play("down")
    play("left")

    try:
        game_over = browser.find_element_by_class_name("game-over")
    except NoSuchElementException:
        continue
    if game_over:
        break

print("Game over!")