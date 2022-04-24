import random 
from Board import Element
from time import sleep
from datetime import datetime
import Settings

class Effecteur():
    def __init__(self, environnement, listhehe, agent):
        self.environnement = environnement
        self.listhehe = listhehe
        self.agent = agent
    
    def go_there(self, pos, action=""):
        print("Je suis en " + str(self.agent.current_position))
        if(action != ""):
            print("Je fais " + action + " sur la position " + str(pos))
        
        self.agent.memoire[self.agent.current_position[0]][self.agent.current_position[1]]["elements"].remove(Element.AGENT)
        self.agent.current_position = pos
        self.agent.memoire[pos[0]][pos[1]]["visited"] = True
        self.agent.memoire[pos[0]][pos[1]]["elements"].append(Element.AGENT)
        
        print("Je vais à " + str(pos) + "\n-------------------")
        if(action == "mourir"):
            print("Fin du jeu : je suis tombé sous les décombres. Adieu...")
            exit(1)

    def do_action(self, pos):
        action = ""
        if (Element.FIRE in self.agent.memoire[pos[0]][pos[1]]["elements"]):
            action = "éteindre le feu"
            self.extinguish_fire(pos)
        elif (Element.RUBBLE in self.agent.memoire[pos[0]][pos[1]]["elements"]):
            action = "mourir"
        return action

    def extinguish_fire(self, fire_pos):
        self.agent.memoire[fire_pos[0]][fire_pos[1]]["elements"].remove(Element.FIRE)
        random.shuffle(self.listhehe)
        for (k, l) in self.listhehe:
            if(self.environnement.isInBornes((fire_pos[0] + k, fire_pos[1] + l)) and Element.HEAT in self.agent.memoire[fire_pos[0] + k][fire_pos[1] + l]["elements"]):
                self.agent.memoire[fire_pos[0] + k][fire_pos[1] + l]["elements"].remove(Element.HEAT)
