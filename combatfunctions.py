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

def findHitOutcome(damage, defence, parry):
    if damage > defence + parry:
        return damage - defence - parry
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

def parryResult(hitlist, defender, start, ws):

    parry_dmg = 0

    i = start + 1

    while i < len(hitlist):
        if hitlist[i][1] == defender:
            if hitlist[i][2] == 0:

                proll = random.randint(1,100)
                    
                if ws >= proll:
                    parry_dmg = random.randint(1,6)
                else:
                    parry_dmg = 0
                
                return parry_dmg
        
        i += 1


    return parry_dmg

def createHitList(hitlist_current, initiative_list, name):

    i = 0

    while i < len(initiative_list):
        
        hitlist_current.append([initiative_list[i], name, 0, name[0]])

        i += 1

    return hitlist_current

def markAttackUsed(hitlist, attacker, start, adjustment):
    i = start + adjustment
    while i < len(hitlist):
        if hitlist[i][1] == attacker:
            hitlist[i][2] = 1
            return hitlist
        i += 1
    return hitlist

def checkSuddenDeath(critical_hit, hit):

    critical_ranges = [9, 20, 30, 40, 50, 100]
    critical_outcomes = [[0,0,0,0,0,1], [0,0,0,0,1,1], [0,0,0,1,1,1], [0,0,1,1,1,1], [0,1,1,1,1,1], [1,1,1,1,1,1,1]]

    critical_roll = random.randint(1,100)

    if critical_hit > 6:
        critical_hit = 6

    i = 0

    while True:

        if critical_roll <= critical_ranges[i]:
            critical_outcome = critical_outcomes[i][critical_hit - 1]
            break
        else:
            i += 1

    if critical_outcome == 1:
        hit_location = findHitLocation(hit)
        message = " blow smashes opponents " + hit_location + ". Death from shock and blood loss is almost instantaneous."
        return [critical_outcome, message]
    else:
        message = "Your opponent is staggered, but recoveres quickly and continues the fight."
        return [critical_outcome, message]