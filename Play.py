# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 20:18:07 2020

@author: RedDevil
"""

import Ships
import Commands
import random


def processNavalCombatAction(action, attackShip, defenseShip):
    if action == "help":
        print("Here are your options:\n")
        print("ahead => Full speed ahead!\n")
        print("half => Half sail!\n")
        print("hold => Hold position!\n")
        print("port => Turn to port!\n")
        print("star => Turn to starboard!\n")
        print("jibe => Prepare to jibe!\n")
        print("fire => Cannons ready!\n")
        print("report => Report to...\n")
        print("brace => Brace for impact!\n")
        print("surrender => We surrender!\n")
        return 1
    # TODO: add accuracy changing based on maneuver
    elif action == "ahead":
        print("Full speed ahead!\n")
        attackShip.speedUp()
        attackShip.move()
        return 1
    elif action == "half":
        print("Half sail!\n")
        attackShip.slowDown()
        attackShip.move()
        return 1
    elif action == "hold":
        print("Hold position!\n")
        return 1
    elif action == "port":
        print("Turn to port!\n")
        attackShip.turn(action)
        return 1
    elif action == "star":
        print("Turn to starboard!\n")
        attackShip.turn(action)
        return 1
    elif action == "jibe":
        print("Prepare to jibe!\n")
        attackShip.turn(action)
        return 1
    elif action == "fire":
        print("Cannons ready!\n")
        distance = 0
        if attackShip.facing == 0 or attackShip.facing == 2:
            distance = abs(attackShip.location[1] - defenseShip.location[1])
        else:
            distance = abs(attackShip.location[0] - defenseShip.location[0])
        damage = -1
        while damage == -1:
            side = input("Which side cannons do you want to fire?\n")
            damage = attackShip.fire(distance, side, defenseShip)
        print(attackShip.name + " dealt " + str(damage) + " damage to " + defenseShip.name + "!\n")
        defenseShip.hullHealth -= damage
        return 1
    # TODO: finish report, brace, and surrender
    elif action == "report":
        print("Report to...NOTWORKINGYET\n")
        return 1
    elif action == "brace":
        print("Brace for impact!NOTWORKINGYET\n")
        return 1
    elif action == "surrender":
        print("We surrender!NOTWORKINGYET\n")
        return 1
    else:
        print("Invalid action. Try again or type help.\n")
        return 0

def navalCombatLoop(Ship1, Ship2):
    inCombat = True
    roundNum = 1
    while inCombat:
        print("ROUND " + str(roundNum) + "!")
        # Determine round initiative
        firstToGo = random.randrange(1,3)
        if firstToGo == 1:
            firstShip = Ship1
            secondShip = Ship2
        else:
            firstShip = Ship2
            secondShip = Ship1
        print(firstShip.name + " will go first this turn.\n")
        turnNum = 1
        while turnNum <= 3:
            # First Ship
            validAction = 0
            while validAction == 0:
                action = input("What would " + firstShip.name + " like to do?\n")
                validAction = processNavalCombatAction(action, firstShip, secondShip)
            # Second Ship
            validAction = 0
            while validAction == 0:
                action = input("What would " + secondShip.name + " like to do?\n")
                validAction = processNavalCombatAction(action, secondShip, firstShip)
            # Check if one of the ships has sunk
            if not firstShip.isAfloat():
                print(firstShip.name + " has disappeared beneath the waves.\n")
                inCombat = False
            elif not secondShip.isAfloat():
                print(secondShip.name + " has disappeared beneath the waves.\n")
                inCombat = False
            turnNum += 1
        roundNum += 1

    


print("Starting game")

curShip = None
result = -1

# Game loop
while result != 0 :
    cmd = input("Ready for command:\n")
    result = Commands.processCommand(cmd)
    if isinstance(result, Ships.Ship) and result is not None:
        curShip = result
        
        