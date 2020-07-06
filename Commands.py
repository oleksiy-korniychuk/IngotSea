# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 21:32:41 2020

@author: RedDevil
"""

import Ships

windSpeed = 15
drag = 5

def processCommand(cmd):
    if cmd == "new ship":
        name = input("What will this ship be called?\n")
        crew = input("How big will the crew of " + name + " be?\n")
        s1 = Ships.Ship(name, crew)
        return s1
    elif cmd == "combat":
        print("This function still needs to be added\n")
    elif cmd == "help":
        print("To create a ship, type 'new ship'\n")
        return 1
    elif cmd == "exit":
        input("Thanks for playing! Press Enter to quit\n")
        return 0
    else:
        print("Sorry, invalid command\n")
        return None