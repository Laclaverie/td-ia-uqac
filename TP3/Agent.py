import random
from datetime import datetime
from Board import Element
from Board import Probabilities
from Capteur import Capteur
from Effecteur import Effecteur

class Agent:
    
    def __init__(self):
        self.levelFinished = False
        self.listhehe = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        random.seed(datetime.now())    
    
    def run(self, environnement):
        self.load_level(environnement)
        while(not self.levelFinished):
            possibilities = self.capteur.check_voisins(self.memoire, self.current_position)
            
            if not self.levelFinished:
                new_pos, action = self.where_to_go(possibilities)
                old_pos = self.current_position
                self.effecteur.go_there(new_pos, action)
                if(new_pos == old_pos):
                    raise Exception("I'm stuck")
            else:
                print("Fin du niveau de taille " + str(self.environnement.size))
        #finito
    
    def get_proba(self, pos, elements, possibilities):
        proba: float = 1
        for element in elements:
            proba *= Probabilities.probabilities[element]

        #partie adjacents de l'adjacent
        prob = 0
        nb = 0
        for (k, l) in self.listhehe:
            if(self.environnement.isInBornes((pos[0] + k, pos[1] + l))):
                prrr = 1
                nb+=1
                for element in possibilities[pos[0] + k][pos[1] + l]["possibilities"]:
                    prrr *= Probabilities.probabilities[element]
                if(possibilities[pos[0] + k][pos[1] + l]["visited"]):
                    prrr *= Probabilities.probabilities["visited"]
                prob += prrr
        
        proba *= prob / nb
        return proba

    def where_to_go(self, possibilities):
        higher_proba: float = -1.0
        higher_x = self.current_position[0]
        higher_y = self.current_position[1]
        
        random.shuffle(self.listhehe)
        for (k, l) in self.listhehe:
            if(self.environnement.isInBornes((self.current_position[0] + k, self.current_position[1] + l)) and not Element.AGENT in self.memoire[self.current_position[0] + k][self.current_position[1] + l]["elements"]):
                proba = self.get_proba((self.current_position[0] + k, self.current_position[1] + l), self.memoire[self.current_position[0] + k][self.current_position[1] + l]["elements"], possibilities)
                if(self.memoire[self.current_position[0] + k][self.current_position[1] + l]["visited"]):
                    proba *= Probabilities.probabilities["visited"]
                if proba > higher_proba:
                    higher_proba = proba
                    higher_x = self.current_position[0] + k
                    higher_y = self.current_position[1] + l
        
        # print(higher_x, higher_y, higher_proba)
        return (higher_x, higher_y), self.effecteur.do_action((higher_x, higher_y))
    
    
    def end_level(self, victim_pos):
        self.levelFinished = True
        self.effecteur.go_there(victim_pos)
        print("On a atteint la victime en " + str(victim_pos))
        
    def load_level(self, environnement):
        self.environnement = environnement
        #write in txt file the environnement repr
        with open("environnement.txt", "w") as f:
            f.write(str(environnement))
        self.capteur = Capteur(environnement, self.listhehe, self)
        self.effecteur = Effecteur(environnement, self.listhehe, self)

        self.memoire = [[{"elements": [Element.EMPTY], "visited": False} for i in range(environnement.size)] for j in range(environnement.size)]
        self.memoire[0][0]["visited"] = True
        self.memoire[0][0]["elements"].append(Element.AGENT)
        self.current_position = (0, 0)
        self.levelFinished = False
