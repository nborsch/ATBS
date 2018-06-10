#! python3
# -*- coding: utf-8 -*-
#
# Solution to Practice Project "Prettified Stopwatch"
# from "Automate The Boring Stuff", by Al Sweigart,
# Chapter 15.
#
# "Expand the stopwatch project from this chapter so 
# that it uses the rjust() and ljust() string methods 
# to “prettify” the output.
# 
# Next, use the pyperclip module introduced in Chapter 6 
# to copy the text output to the clipboard so the user 
# can quickly paste the output to a text file or email."
# 
# Nadia Borsch      misc@nborsch.com        Jun/2018

import time, pyperclip

print(f"\n{'Prettified Stopwatch':>45}")
print(f"{'********** *********':>45}\n")

# Display program usage instructions
print("* Press ENTER to begin.\n"
    "* Press ENTER to 'click' the stopwatch.\n"
    "* To quit, press c + ENTER.\n"
    "* Final results will be copied to the clipboard.")

# Start the stopwatch the first time
click = input()
if click.lower() == "c":
    print("Done.")
    quit()
else:
    print("Stopwatch started.")
    start_time = time.time()
    last_time = start_time
    laps = 1

# Start second lap onwards
while True:
    click = input()
    if click.lower() == "c":
        break
    
    lap_time = round(time.time() - last_time, 4)
    total_time = round(time.time() - start_time, 4)
    print(f"Lap #{laps:>2}: {total_time:>7} ({lap_time:>7})", end="")
    last_time = time.time()
    laps += 1

pyperclip.copy(f"Laps: {laps:>2} | Total time: {total_time:>7}")
print("\nStopwatch stopped.\n"
        f"* Laps: {laps}\n"
        f"* Total time: {total_time}")
