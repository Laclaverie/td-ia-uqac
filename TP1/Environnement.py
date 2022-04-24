import random
import threading
from enum import IntEnum
import time
from datetime import datetime
import Settings

def contents_to_string(contents):
    tmp= ""
    for el in contents["contents"]:
        tmp+= enum_to_string(el) + " "
    return tmp
def enum_to_string(enum):
    """convert an enum to a string"""
    if(enum == Element.JEWEL):
        return "J"
    elif enum == Element.DIRT:
        return "D"
    elif enum == Element.ROBOT:
        return "R"
    return ""

class Element(IntEnum):
    EMPTY = 0
    JEWEL = 1
    DIRT = 2
    ROBOT = 3

class Environnement:
    def __init__(self, taille, freq):
        random.seed(datetime.now())
        weight_matrix = [[2,5,4,1,4],[3,8,6,1,4],[2,4,9,4,8],[12,1,3,6,5],[3,5,9,4,2]]
        self.taille = taille
        self.map = [[{"contents":[], "weight":weight_matrix[i][j]} for i in range(taille)] for j in range(taille)]
        self.nb_objets = {Element.JEWEL: 0, Element.DIRT: 0}
        self.thread_running = False
        self.last_robot_position = None
        self.freq_generation = freq
        self.thread = None
        self.start_thread()
        
    def __repr__(self):
        # simple_map = [[[int(el) for el in self.map[i][j]["contents"]] for j in range(self.taille)] for i in range(self.taille)]
        tmp_string = ""
        for i in range(self.taille):
                tmp_string += "--------"
        tmp_string += "-\n"
        for row in self.map:
            tmp_string += "| "
            for contents in row:
                tmp_string += f'{contents_to_string(contents): <6}| '
            tmp_string += "\n"
            for i in range(self.taille):
                tmp_string += "--------"
            tmp_string += "-\n"
        return tmp_string
        
    def start_thread(self):
        self.thread_running = True
        self.thread = threading.Thread(target=self.run_env)
        self.thread.start()
        
    def stop_thread(self):
        self.thread_running = False
        self.thread.join()
        print("[Console] - Thread de l'environnement arrêté")        
        
    def run_env(self):
        while (self.thread_running):
            time.sleep(self.freq_generation)
            for el in [Element.DIRT, Element.JEWEL]:
                if self.should_generate(el):
                    self.generate(el)
                
    def should_generate(self, element_type):
        """decide si on doit generer de la poussiere ou du diamant"""
        if self.nb_objets[element_type] >= self.taille * self.taille:
            return False
        if(element_type == Element.DIRT): 
            return random.random() < 0.15
        elif(element_type == Element.JEWEL): 
            return random.random() < 0.05
        return False
            
    def generate(self, object_type):
        """genère de la poussiere ou des diamants à une position non déjà occupée par cet objet"""
        x = random.randint(0, self.taille - 1)
        y = random.randint(0, self.taille - 1)
        while(object_type in self.map[x][y]["contents"]):
            x = random.randint(0, self.taille - 1)
            y = random.randint(0, self.taille - 1)
        if Settings.globalList[0]:
            print("[Environnement] - Je genere un " + str(object_type) + " en " + str(x) + ", " + str(y))
        self.map[x][y]["contents"].append(object_type)
        self.nb_objets[object_type] += 1
        
        if(Settings.globalList[0]):
            print(self, flush=True)