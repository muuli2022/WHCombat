from browser import document, bind
from browser.html import P, BR, B
from dataclasses import dataclass

import random
import combatfunctions as cf

@dataclass
class Opponent:
    name: str = "dummy"
    WS: int = 80
    S: int = 4
    T: int = 3
    W: int = 7
    I: int = 40
    A: int = 2
    parry: bool = False
    sudden_death: bool = False

    def throwDamage(self):
        a = random.randint(1, 6)

        if a == 6: # extradamage
            return self.extraDamage()
        else:
            return a + self.S

    def extraDamage(self):
        damage = 6

        if random.randint(1,100) < self.WS:
            
            docOutput("Extra damage!", "bold")
            roll = random.randint(1,6)
            while roll == 6:
                docOutput("More extra damage", "bold")
                damage += 6
                roll = random.randint(1,6)

            damage += roll

        return damage + self.S

@bind(document["set_Bertold"], "click")
def setBertold(ev):

    document['n_d'].value = "Bertold"
    document['ws_d'].value = "69"
    document['s_d'].value = "7"
    document['t_d'].value = "12"
    document['w_d'].value = "13"
    document['i_d'].value = "63"
    document['a_d'].value = "4"
 
    setAttributesOf(defender, "d")

    docOutput("Bertold set")

@bind(document["set_Michael"], "click")
def setMichael(ev):

    document['n_d'].value = "Michael"
    document['ws_d'].value = "79"
    document['s_d'].value = "10"
    document['t_d'].value = "10"
    document['w_d'].value = "14"
    document['i_d'].value = "58"
    document['a_d'].value = "4"

    setAttributesOf(defender, "d")

    docOutput("Michael set")

# @bind(document["test"], "click")
# def test(ev):

#     if document['inout_a1'].checked:
#         document['inout_a1'].checked = False
#     else:
#         document['inout_a1'].checked = True

@bind(document["round"], "click")
def round(ev):
    
    setAttributesOf(defender, "d")
   

    defender_initiatives = cf.calculateInitiatives(defender.I, defender.A)

    hitlist = getHitlist(attackers)    

    hitlist = cf.createHitList(hitlist, defender_initiatives, "d")

    hitlist.sort(reverse=True)


    defenders = ["d"]
    combatants = attackers + defenders
    

    hitlist = updateRoundStatusToHitlist(hitlist, combatants)    

    document["output"] <= P(B(runCombatRound(hitlist)))

    document["output"].scrollTop = document["output"].scrollHeight

@bind(document["sudden_death"], "click")
def suddenDeath(ev):
    attacker.sudden_death = document["sudden_death"].checked


@bind(document["parry_d"], "click")
def defenderParry(ev):
    defender.parry = document["parry_d"].checked

def addAttackerInOutHandler(i):
    @bind(document[f"inout_a{i}"], "click")
    def attackerInOut(ev):
        
        if attackers.count(f"a{i}") == 0:
            attackers.append(f"a{i}")
        else:
            attackers.remove(f"a{i}")


for i in range(1, 5):
    addAttackerInOutHandler(i)

def docOutput(string, styling=None):
    
    if styling == "bold":
        document["output"] <= B(string)
        document["output"] <= BR()
    else:
        document["output"] <= (string)
        document["output"] <= BR()


def setAttributesOf(opponent, suffix):
    opponent.name = document['n_' + suffix].value
    opponent.WS = int(document['ws_' + suffix].value)
    opponent.S = int(document['s_' + suffix].value)
    opponent.T = int(document['t_' + suffix].value)
    opponent.W = int(document['w_' + suffix].value)
    opponent.I = int(document['i_' + suffix].value)
    opponent.A = int(document['a_' + suffix].value)
    
    if suffix != "d":
        opponent.parry = document['parry_' + suffix].checked


def getHitlist(attackers):

    hitlist = []
    i = 0
    while i < len(attackers):

        temp_initiative = cf.calculateInitiatives(int(document['i_' + attackers[i]].value), int(document['a_' + attackers[i]].value))
        hitlist = cf.createHitList(hitlist, temp_initiative, attackers[i])
        i += 1
    
    hitlist.sort(reverse=True)
    
    return hitlist


def saveRoundStatus(hitlist, attackers, isend):

    defenders = ["d"]

    combatants = attackers + defenders

    if isend == 0:
        i = 0

        while i < len(combatants):
            k = 0
            temp = 0
            while k < len(hitlist):
                if hitlist[k][1] == combatants[i]:
                    temp = temp + hitlist[k][2]
                k += 1
            document['ua_' + combatants[i]].value = str(temp)
            i += 1
    else:

        i = 1

        while i < 5:
            document['ua_' + 'a' + str(i)].value  = "0"
            
            i += 1

        document['ua_d'].value  = "0"

    return

def updateRoundStatusToHitlist(hitlist, combatants):

    i = 0

    while i < len(combatants):

        k = 0
        j = 0
        while k < len(hitlist):
            
            if hitlist[k][1] == combatants[i]:
                if j == int(document['ua_' + combatants[i]].value):
                    break
                hitlist[k][2] = 1
                j += 1

            k += 1

        i += 1
  
    return hitlist      

def runCombatRound(hitlist):
    i = 0
    attacks = len(hitlist)
 
    message = ""

    while i < attacks:

        if hitlist[i][3] == "a":
            setAttributesOf(attacker, hitlist[i][1])
            if hitlist[i][2] == 0:
                message = attacker.name + " hits on initiative " + str(hitlist[i][0])
                docOutput(message)
                
                hitlist = cf.markAttackUsed(hitlist, hitlist[i][1], i, 0)
                
                hit = random.randint(1,100)
                
                message = attacker.name + " threw " + str(hit)
                docOutput(message)

                if hit <= attacker.WS:

                    message = attacker.name + " hits " + str(cf.findHitLocation(hit))
                    docOutput(message)
                    
                    damage = attacker.throwDamage()

                    parry_outcome = 0

                    if defender.parry:
                        parry_outcome = cf.parryResult(hitlist, "d", i, defender.WS)
                        
                        hitlist = cf.markAttackUsed(hitlist, "d", i, 0)
                        
                        if parry_outcome > 0:
                            message = defender.name + " parried " + str(parry_outcome) + " points of damage."
                            docOutput(message)
                        else:
                            message = defender.name + "'s parry was unsuccesful."
                            docOutput(message)

                    outcome = cf.findHitOutcome(damage, defender.T, parry_outcome) 

                    message = attacker.name + " did " + str(damage) + " points damage and " + defender.name + " lost " + str(outcome) + " wounds"
                    docOutput(message)
                    defender.W -= outcome

                    document['w_d'].value = str(defender.W)

                    if defender.W < 0:
                        temp = str(defender.W)

                        criticalHit = "+" + temp[1:]
                        defender.W = 0
                        document['w_d'].value = str(defender.W)

                        message = defender.name + " suffers " + criticalHit + " critical hit. Throw a critical effect!"
                        saveRoundStatus(hitlist, attackers, 0)
                        return message
                    else:
                        message = defender.name + " has " + str(defender.W) + " wounds left."
                        docOutput(message)

                else:
                    
                    if cf.checkFumble(hit) == "Miss!":
                        docOutput("Miss!")
                    else:
                        message = attacker.name + " fumbled with roll " + str(hit) + ". Loose one attack."
                        docOutput(message, "bold")
                        hitlist = cf.markAttackUsed(hitlist, hitlist[i][1], i, 1)
               
            else:
                message = attacker.name + " has already used action on initiative " + str(hitlist[i][0])
                docOutput(message)

            i += 1
        else:
            setAttributesOf(defender, "d")
            if hitlist[i][2] == 0:
                message = defender.name + " hits on initiative " + str(hitlist[i][0])
                docOutput(message)

                hitlist = cf.markAttackUsed(hitlist, "d", i, 0)

                setAttributesOf(attacker, attackers[0])

                hit = random.randint(1,100)
                
                message = defender.name + " threw " + str(hit)
                docOutput(message)

                if hit <= defender.WS:
                    message = defender.name + " hits " + str(cf.findHitLocation(hit))
                    docOutput(message)

                    damage = defender.throwDamage()

                    parry_outcome = 0

                    if attacker.parry:
                        
                        parry_outcome = cf.parryResult(hitlist, attackers[0], i, attacker.WS)
                        
                        hitlist = cf.markAttackUsed(hitlist, attackers[0], i, 0)

                        if parry_outcome > 0:
                            message = attacker.name + " parried " + str(parry_outcome) + " points of damage."
                            docOutput(message)
                        else:
                            message = attacker.name + "'s parry was unsuccesful."
                            docOutput(message)

                    outcome = cf.findHitOutcome(damage, attacker.T, parry_outcome)

                    message = defender.name + " did " + str(damage) + " points damage and " + attacker.name + " lost " + str(outcome) + " wounds"
                    docOutput(message)

                    attacker.W -= outcome

                    document['w_' + attackers[0]].value = str(attacker.W)

                    if attacker.W < 0:
                        
                        temp = str(attacker.W)

                        criticalHit = "+" + temp[1:]
                        attacker.W = 0
                        document['w_' + attackers[0]].value = str(attacker.W)

                        if attacker.sudden_death:

                            critical_outcome = cf.checkSuddenDeath(int(temp[1:]), hit)

                            if critical_outcome[0] == 1:

                                message = defender.name + "'s" + critical_outcome[1]
                                saveRoundStatus(hitlist, attackers, 0)

                                document['inout_' + attackers[0]].checked = False

                                attackers.remove(attackers[0])
                                return message
                            else:
                                message = critical_outcome[1]
                                docOutput(message, "bold")
                        else:
                        
                            message = attacker.name + " suffers " + criticalHit + " critical hit. Throw a critical effect!"
                            saveRoundStatus(hitlist, attackers, 0)

                            return message
                        
                    else:
                        message = attacker.name + " has " + str(attacker.W) + " wounds left."
                        docOutput(message)

                else:
                    
                    if cf.checkFumble(hit) == "Miss!":
                        docOutput("Miss!")
                    else:
                        message = defender.name + " fumbled with roll " + str(hit) + ". Loose one attack."
                        docOutput(message, "bold")
                        hitlist = cf.markAttackUsed(hitlist, hitlist[i][1], i, 1)

            else:
                message = defender.name + " has already used action on initiative " + str(hitlist[i][0])
                docOutput(message)

            i += 1


    saveRoundStatus(hitlist, attackers, 1)
    
    return "Attacks done!"



# Program running starts here

defender = Opponent()
    
attacker = Opponent()

attackers = []





