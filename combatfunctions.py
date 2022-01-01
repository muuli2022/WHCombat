#functions for Warhammer combat

import random

def calculateInitiatives(init : int, a : int):

    initiatives = []
    i = 0
    while i < a:
        initiatives.append(int(init/a*(a-i)))
        i += 1

    return initiatives

def throwHit(ws : int):

    a = random.randint(1,100)

    result = []

    if ws >= a:
        result = ["Hit!", str(a)]
        return result
    else:
        result = [checkFumble(a), str(a)]
        return result

def findHitLocation(hit : int):
    
    hitlocations = [15, 35, 55, 80, 90, 100]
    hitlocationnames = ["Head", "Right Arm", "Left Arm", "Body", "Left Leg", "Right Leg"]

    temp = str(hit)

    if len(temp) == 2:
        hitlocation = int(temp[1] + temp[0])
    else:
        hitlocation = int(temp + "0")
    
    i = 0

    while True:

        if hitlocation <= hitlocations[i]:
            return hitlocationnames[i]
        else:
            i += 1

def findHitOutcome(damage, defence):
    if damage > defence:
        return damage - defence
    else:
        return 0

def checkFumble(hit : int):

    temp = str(hit)
    
    if len(temp) == 1:
        return "Miss!"

    if hit == 100:
        return "Fumble!"

    if temp[0] == temp[1]:
        return "Fumble!"

    return "Miss!"