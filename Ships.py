# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 19:56:02 2020

@author: RedDevil
"""

import random

class Cannon:
    minRange = 0
    maxRange = 0
    minDamage = 0
    maxDamage = 0
    reloadSpeed = 1 # In number of turns

    turnsLeft = 0   # Number of turns left until ready to fire. Ready at 0

    def __init__(self, minRange = 0, maxRange = 0, minDamage = 0, maxDamage = 0, reloadSpeed = 1):
        self.minRange = minRange
        self.maxRange = maxRange
        self.minDamage = minDamage
        self.maxDamage = maxDamage
        self.reloadSpeed = reloadSpeed

    # Returns damage if the cannon can fire and -1 if the cannon is not loaded
    def fire(self):
        damage = -1
        if self.turnsLeft == 0:
            damage = random.randrange(self.minDamage, self.maxDamage + 1)
            self.turnsLeft = self.reloadSpeed
        return damage

    # Returns True if done reloading and False if still reloading
    def reload(self):
        if self.turnsLeft == 0:
            return True
        else:
            self.turnsLeft -= 1
            return False

    def inRange(self, distance):
        if self.minRange <= distance <= self.maxRange:
            return True
        else:
            return False

class Ship:
    'Base class for all ships or vessels meant to carry animate creatures through the water'
    name = ""
    numCrew = 1
    crewList = []
    weightStored = 0
    cargoList = []
    baseSpeed = 0
    hullHealth = 1

    portCannon = Cannon()
    starCannon = Cannon()

    currentSpeed = 0
    facing = 0 # 0 = north, 1 = east, 2 = south, 3 = wests
    location = [0,0]
    accuracy = 0
    
    def __init__(self, name, numCrew = 1, crewList = [], weightStored = 0, cargoList = [], baseSpeed = 1, hullHealth = 1):
        self.name = name
        self.numCrew = numCrew
        self.crewList = crewList
        self.weightStored = weightStored
        self.cargoList = cargoList
        self.baseSpeed = baseSpeed
        self.hullHealth = hullHealth

    def addCrew(self, newCrewList):
        self.numCrew += len(newCrewList)
        self.crewList.extend(newCrewList)

    def addCargo(self, newCargoList):
        for item in newCargoList:
            self.weightStored += item.weight
        self.cargoList.extend(newCargoList)

    def setName(self, newName):
        self.name = newName

    def setFacing(self, newFacing):
        self.facing = newFacing

    def move(self):
        if self.facing == 1:
            self.location[1] -= self.currentSpeed
        elif self.facing == 2:
            self.location[0] += self.currentSpeed
        elif self.facing == 3:
            self.location[1] += self.currentSpeed
        else: #facing == 4
            self.location[0] -= self.currentSpeed

    def turn(self, direction):
        if direction == "port":
            self.facing = (self.facing - 1)%4
        elif direction == "star":
            self.facing = (self.facing + 1)%4
        elif direction == "jibe":
            self.facing = (self.facing + 2)%4

    def slowDown(self):
        if self.currentSpeed - self.baseSpeed <= 0:
            self.currentSpeed = 0
        else:
            self.currentSpeed -= self.baseSpeed

    def speedUp(self):
        self.currentSpeed =+ self.baseSpeed

    #TODO: Need to account for the side matching up with the direction of the enemy ship
    def fire(self, distance, side, targetShip):
        damage = 0
        if side == "port" and self.portCannon.inRange(distance):
            damage = self.portCannon.fire()
        elif side == "star" and self.starCannon.inRange(distance):
            damage = self.starCannon.fire()
        else:
            print("Invalid side. Try again.\n")
            return -1
        return damage

    def reload(self):
        if not self.portCannon.reload():
            print(str(self.portCannon.turnsLeft) + " turns left before the port side cannon is ready.\n")
        else:
            print("Port side cannon is ready to fire!\n")
        if not self.starCannon.reload():
            print(str(self.starCannon.turnsLeft) + " turns left before the starboard cannon is ready.\n")
        else:
            print("Starboard cannon is ready to fire!\n")

    def isAfloat(self):
        if self.hullHealth > 0:
            return True
        else:
            return False
