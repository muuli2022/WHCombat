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
    parry: str = "off"

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


@bind(document["set_attributes"], "click")
def setAttributes(ev):

    setAttributesOf(attacker, "a")
    setAttributesOf(defender, "d")

    docOutput("Attributes set")

@bind(document["set_Bertold"], "click")
def setAttributes(ev):

    document['n_d'].value = "Bertold"
    document['ws_d'].value = "69"
    document['s_d'].value = "7"
    document['t_d'].value = "12"
    document['w_d'].value = "13"
    document['i_d'].value = "63"
    document['a_d'].value = "4"
 
    docOutput("Bertold set")

@bind(document["set_Michael"], "click")
def setAttributes(ev):

    document['n_d'].value = "Michael"
    document['ws_d'].value = "79"
    document['s_d'].value = "10"
    document['t_d'].value = "10"
    document['w_d'].value = "14"
    document['i_d'].value = "58"
    document['a_d'].value = "4"

    docOutput("Michael set")

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

def runCombatRound(att_inits, def_inits, attacks):
    i = 0
    ai = 0
    di = 0

    message = ""

    while i < attacks:

        if att_inits[ai] > def_inits[di]:
            
            message = attacker.name + " hits on initative " + str(att_inits[ai])
            docOutput(message)
            
            ai += 1
 
            hit = random.randint(1,100)

            message = attacker.name + " threw " + str(hit)
            docOutput(message)

            if hit <= attacker.WS:

                message = attacker.name + " hits " + str(cf.findHitLocation(hit))
                docOutput(message)
                
                #docOutput("paikka a.0.5")

                damage = attacker.throwDamage()

                parry_outcome = 0

                if defender.parry == "on":
                    parry_outcome = cf.parryResult(di,defender.WS, defender.A)
                    di += 1
                    attacks -= 1

                    if parry_outcome > 0:
                        message = defender.name + " parried " + str(parry_outcome) + " points of damage."
                        docOutput(message)
                    else:
                        message = defender.name + "'s parry was unsuccesful."
                        docOutput(message)

                #docOutput("paikka a.2")

                outcome = cf.findHitOutcome(damage, defender.T, parry_outcome) 

                #docOutput("paikka a.3")

                message = attacker.name + " did " + str(damage) + " points damage and " + defender.name + " lost " + str(outcome) + " wounds"
                docOutput(message)
                defender.W -= outcome

                if defender.W < 0:
                    temp = str(defender.W)

                    criticalHit = "+" + temp[1:]
                    defender.W = 0

                    return defender.name + " suffers " + criticalHit + " critical hit. Throw a critical effect!"
                else:
                    message = defender.name + " has " + str(defender.W) + " wounds left."
                    docOutput(message)

            else:
                
                if cf.checkFumble(hit) == "Miss!":
                    docOutput("Miss!")
                else:
                    message = attacker.name + " fumbled with roll " + str(hit) + ". Loose one attack."
                    docOutput(message, "bold")
                    if ai < len(att_inits) - 1:
                        ai +=1
                        attacks -= 1
        else:
            message = defender.name + " hits on initative " + str(def_inits[di])
            docOutput(message)
            
            di += 1
 
            hit = random.randint(1,100)

            message = defender.name + " threw " + str(hit)
            docOutput(message)

            if hit <= defender.WS:
                parry_outcome = 0
                message = defender.name + " hits " + str(cf.findHitLocation(hit))
                docOutput(message)
                #docOutput("paikka d.0.5")
                damage = defender.throwDamage()

                parry_outcome = 0

                if attacker.parry == "on":
                    parry_outcome = cf.parryResult(ai,attacker.WS, attacker.A)
                    ai += 1
                    attacks -= 1

                    if parry_outcome > 0:
                        message = attacker.name + " parried " + str(parry_outcome) + " points of damage."
                        docOutput(message)
                    else:
                        message = attacker.name + "'s parry was unsuccesful."
                        docOutput(message)



                #docOutput("paikka d.1")
                outcome = cf.findHitOutcome(damage, attacker.T, parry_outcome)
                #docOutput("paikka d.2")
                message = defender.name + " did " + str(damage) + " points damage and " + attacker.name + " lost " + str(outcome) + " wounds"
                #docOutput("paikka d.3")
                
                docOutput(message)
                attacker.W -= outcome

                if attacker.W < 0:
                    
                    temp = str(attacker.W)

                    criticalHit = "+" + temp[1:]
                    attacker.W = 0

                    return attacker.name + " suffers " + criticalHit + " critical hit. Throw a critical effect!"
                     
                else:
                    message = attacker.name + " has " + str(attacker.W) + " wounds left."
                    docOutput(message)

            else:
                
                if cf.checkFumble(hit) == "Miss!":
                    docOutput("Miss!")
                else:
                    message = defender.name + " fumbled with roll " + str(hit) + ". Loose one attack."
                    docOutput(message)
                    if di < len(def_inits) - 1:
                        di +=1
                        attacks -= 1

        i += 1

    return "Attacks done"

@bind(document["round"], "click")
def round(ev):
    
    defender_initiatives = cf.calculateInitiatives(defender.I, defender.A)
    attacker_initiatives = cf.calculateInitiatives(attacker.I, attacker.A)

    i = 0
    all_attacks = attacker.A + defender.A
    


    defender_initiatives.append(0)
    attacker_initiatives.append(0)

    document["output"] <= P(B(runCombatRound(attacker_initiatives, defender_initiatives, all_attacks)))


    document["output"].scrollTop = document["output"].scrollHeight

@bind(document["parry_a"], "click")
def checkboxtest(ev):
    if attacker.parry == "off":
        attacker.parry = "on"
    else:
        attacker.parry = "off"

@bind(document["parry_d"], "click")
def checkboxtest(ev):
    if defender.parry == "off":
        defender.parry = "on"
    else:
        defender.parry = "off"

# Program running starts here

defender = Opponent()
    
attacker = Opponent()



