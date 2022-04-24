import random 
from Environnement import Element
from time import sleep
from datetime import datetime
import Settings

class Effecteur():
    def __init__(self, environnement):
        random.seed(datetime.now())
        x = random.randint(0, environnement.taille - 1)
        y = random.randint(0, environnement.taille - 1)
        self.position = [x, y]
        self.environnement = environnement

    def move_robot(self):
        self.move_robot_to(self.position)
        
    def move_robot_to(self, position):
        """place le robot dans l'environnement à la position donnee en parametre"""
        if(self.environnement.last_robot_position is not None):
            self.environnement.map[self.environnement.last_robot_position[0]][self.environnement.last_robot_position[1]]["contents"].remove(
                Element.ROBOT)  # enlève le robot de la case qu'il occupait précédemment
        self.environnement.map[position[0]][position[1]]["contents"].append(Element.ROBOT)
        
        if Settings.globalList[0]:
            print(self.environnement, flush=True)
        self.environnement.last_robot_position = position
    
    def decide_what_to_do(self):
        """decide d'aspirer ou de ramasser en fonction de l'objet sur la case"""
        if Settings.globalList[0]:
            print("[Effecteur] - Je decide de quoi faire sur la case")
        if(Element.DIRT in self.environnement.map[self.position[0]][self.position[1]]["contents"]):
            return self.vacuum()
        elif(Element.JEWEL in self.environnement.map[self.position[0]][self.position[1]]["contents"]):
            return self.get_jewel()
        
    def vacuum(self):
        if Settings.globalList[0]:
            print("[Effecteur] - J'aspire le sol")
        """aspire la poussiere et les bijoux"""
        self.environnement.map[self.position[0]][self.position[1]]["contents"].remove(Element.DIRT)
        self.environnement.nb_objets[Element.DIRT] -= 1
        try:
            self.environnement.map[self.position[0]][self.position[1]]["contents"].remove(Element.JEWEL)
            self.environnement.nb_objets[Element.JEWEL] -= 1
        except:
            pass
        if Settings.globalList[0]:
            #IMPORTANT: ce sleep permet d'avoir le temps de voir le déplacement de l'agent avant de faire l'action
            sleep(0.35)
            print(self.environnement, flush=True)
        
    def get_jewel(self):
        if Settings.globalList[0]:
            print("[Effecteur] - Je ramasse les bijoux")
        """ramasse le bijoux"""
        self.environnement.map[self.position[0]][self.position[1]]["contents"].remove(Element.JEWEL)
        self.environnement.nb_objets[Element.JEWEL] -= 1
        
        if Settings.globalList[0]:
            #IMPORTANT: ce sleep permet d'avoir le temps de voir le déplacement de l'agent avant de faire l'action
            sleep(0.35)
            print(self.environnement, flush=True)
        
    def update_position(self, position):
        """met à jour la position"""
        if Settings.globalList[0]:
            print("[Effecteur] - Je met à jour ma position")
        self.position = position
