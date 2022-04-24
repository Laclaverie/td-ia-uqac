import random
import sys
import math
from math import floor
from datetime import datetime
from enum import IntEnum


class Element(IntEnum):
    EMPTY = 0
    FIRE = 1
    HEAT = 2
    RUBBLE = 3
    DIRT = 4
    AGENT = 5
    VICTIM = 6
    CRIES = 7

class Probabilities:
    
    probabilities = {
        Element.EMPTY: 0.8,
        Element.FIRE: 0.5,
        Element.RUBBLE: 0.01,
        Element.VICTIM: 10,
        Element.HEAT: 0.7,
        Element.DIRT: 0.4,
        Element.CRIES: 3.0,
        "visited": 0.0
        }

def enu_to_string(enum):
    """convert an enum to a string"""
    if enum == Element.FIRE:
        return "F"
    elif enum == Element.HEAT:
        return "H"
    elif enum == Element.RUBBLE:
        return "R"
    elif enum == Element.DIRT:
        return "D"
    elif enum == Element.AGENT:
        return "A"  # Agent
    elif enum == Element.VICTIM:
        return "V"
    elif enum == Element.CRIES:
        return "W"
    return ""


def contents_to_string(contents):
    tmp = ""
    for el in contents["contents"]:
        tmp += enu_to_string(el) + " "
    return tmp


class Board:
    def __init__(self, size):
        """
        Constructeur de la classe Board
        """
        self.size = size
        self.fire_proportion = floor(size/2)  # proportion de foyer (n/proportion)
        # proportion de decombres (n/proportion)
        self.rumble_proportion = floor(size/2)
        random.seed(datetime.now())
        self.grid = [[[Element.EMPTY, Element.EMPTY, Element.EMPTY]] * size for i in range(size)]
        self.map = [[{"contents": []} for i in range(self.size)] for j in range(self.size)]
        self.random_valid_board()
        self.last_robot_position = [0, 0]

    def random_valid_board(self):
        """
        Genere une grille dans laquelle va representer l'environnement

        :return:
        """
        # creation d'une grille vide
        self.map[0][0]["contents"].append(Element.AGENT)  # CONSIGNE
        # ajouter la personne a secourir
        ok = False
        while not ok:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)

            if Element.AGENT not in self.map[x][y]["contents"] and Element.RUBBLE not in self.map[x][y]["contents"] and Element.FIRE not in self.map[x][y]["contents"] and Element.VICTIM not in self.map[x][y]["contents"]:
                self.map[x][y]["contents"].append(Element.VICTIM)
                self.fill_with_cries(x,y)
                ok = True
                
        # Ajouter du feu
        fin = self.fire_proportion + 1
        for i in range(random.randint(1, fin)):
            ok = False
            while not ok:
                x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)

                if Element.AGENT not in self.map[x][y]["contents"] and Element.RUBBLE not in self.map[x][y]["contents"] and Element.FIRE not in self.map[x][y]["contents"] and Element.VICTIM not in self.map[x][y]["contents"]:  # rien dedans
                    self.map[x][y]["contents"].append(Element.FIRE)
                    self.fill_with_heat(x, y)
                    ok = True

        # Ajouter des debris
        fin2 = self.rumble_proportion + 1
        for i in range(random.randint(1, fin2)):
            ok = False
            while not ok:
                x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
                if Element.AGENT not in self.map[x][y]["contents"] and Element.RUBBLE not in self.map[x][y]["contents"] and Element.FIRE not in self.map[x][y]["contents"] and Element.VICTIM not in self.map[x][y]["contents"]:
                    self.map[x][y]["contents"].append(Element.RUBBLE)
                    self.fill_with_dust(x, y)
                    ok = True

        

    def __repr__(self):
        # simple_map = [[[int(el) for el in self.map[i][j]["contents"]] for j in range(self.size)] for i in range(self.size)]
        tmp_string = ""
        for i in range(self.size):
            tmp_string += "--------"
        tmp_string += "-\n"
        for row in self.map:
            tmp_string += "| "
            for contents in row:
                tmp_string += f'{contents_to_string(contents): <6}| '
            tmp_string += "\n"
            for i in range(self.size):
                tmp_string += "--------"
            tmp_string += "-\n"
        return tmp_string

    def fill_with_heat(self, x, y):
        """
        Un feu se trouve en (x,y) on remplit les cotes adjascent par de la chaleur
        :param x: ligne
        :param y: colonne
        :return: None (mets a jour self.map)
        """
        if x - 1 >= 0:
            self.map[x - 1][y]["contents"].append(Element.HEAT)
        if x + 1 <= self.size - 1:
            self.map[x + 1][y]["contents"].append(Element.HEAT)
        if y - 1 >= 0:
            self.map[x][y - 1]["contents"].append(Element.HEAT)

        if y + 1 <= self.size - 1:
            self.map[x][y + 1]["contents"].append(Element.HEAT)

    def fill_with_dust(self, x, y):
        """
        Un debris se trouve en x,y on remplit les cotes adjascent par de la poussiere
        :param x: ligne
        :param y: colonne
        :return: None (mets a jour self.map)
        """
        if x - 1 >= 0:
            self.map[x - 1][y]["contents"].append(Element.DIRT)
        if x + 1 <= self.size - 1:
            self.map[x + 1][y]["contents"].append(Element.DIRT)
        if y - 1 >= 0:
            self.map[x][y - 1]["contents"].append(Element.DIRT)
        if y + 1 <= self.size - 1:
            self.map[x][y + 1]["contents"].append(Element.DIRT)

    def fill_with_cries(self,x,y):
        """
        Une victime se trouve en x,y , rempli les cotes adjascents de ses cris
        :param x: ligne
        :param y: colonne
        :return: None (mets a jour la map)
        """
        if x - 1 >= 0:
            self.map[x - 1][y]["contents"].append(Element.CRIES)
        if x + 1 <= self.size - 1:
            self.map[x + 1][y]["contents"].append(Element.CRIES)
        if y - 1 >= 0:
            self.map[x][y - 1]["contents"].append(Element.CRIES)
        if y + 1 <= self.size - 1:
            self.map[x][y + 1]["contents"].append(Element.CRIES)

    def isInBornes(self, pos):
        """
        Verifie si la position est dans les bornes de la grille
        :param pos: la position a verifier
        :return: True si dans les bornes, False sinon
        """
        return pos[0] >= 0 and pos[0] < self.size and pos[1] >= 0 and pos[1] < self.size
