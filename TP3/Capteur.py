import random
from datetime import datetime
from Board import Element
class Capteur():
    def __init__(self, environnement, listhehe, agent):
        self.environnement = environnement
        self.listhehe = listhehe
        self.agent = agent
        random.seed(datetime.now())

    def check_voisins(self, agent_memoire, current_position):

        i, j = current_position
        possibilities = [[{"position": (o, p), "possibilities": [], "nonpossibilities": [
        ], "visited": False, "determined": False} for o in range(self.environnement.size)] for p in range(self.environnement.size)]
        agent_memoire[i][j]["visited"] = True
        possibilities[i][j]["visited"] = True

        random.shuffle(self.listhehe)
        for (k, l) in self.listhehe:
            if(self.environnement.isInBornes((i + k, j + l))):
                if(self.environnement.map[i + k][j + l]["contents"] == [Element.EMPTY]):
                    break

                for element in self.environnement.map[i + k][j + l]["contents"]:
                    if(element == Element.AGENT):
                        break
                    agent_memoire[i + k][j + l]["elements"].append(element)
                    if(element == Element.VICTIM):
                        self.agent.end_level((i + k, j + l))
                    elif(element == Element.FIRE or Element.RUBBLE):
                        possibilities[i + k][j +
                                             l]["possibilities"] = [element]
                        possibilities[i + k][j + l]["determined"] = True
                    if(element != Element.EMPTY):
                        self.check_positive_subsequent_cases(
                            i + k, j + l, abs(k) == 1, element, possibilities)  # supposition
                        self.check_negative_subsequent_cases(
                            i + k, j + l, abs(k) == 1, element, possibilities)  # supposition
        return possibilities

    def check_positive_subsequent_cases(self, a, b, horizontal, element, possibilities):
        for m in [1, -1]:
            if(horizontal):
                b += m
            else:
                a += m
            if(not self.environnement.isInBornes((a, b)) or possibilities[a][b]["determined"] or possibilities[a][b]["visited"]):
                break
            if(element == Element.HEAT and Element.FIRE not in possibilities[a][b]["nonpossibilities"]):
                possibilities[a][b]["possibilities"].append(Element.FIRE)
            elif(element == Element.CRIES and Element.CRIES not in possibilities[a][b]["nonpossibilities"]):
                possibilities[a][b]["possibilities"].append(Element.VICTIM)
            elif(element == Element.DIRT and Element.DIRT not in possibilities[a][b]["nonpossibilities"]):
                possibilities[a][b]["possibilities"].append(Element.RUBBLE)

    def check_negative_subsequent_cases(self, a, b, horizontal, element, possibilities):
        random.shuffle(self.listhehe)
        for (k, l) in self.listhehe:
            if(not self.environnement.isInBornes((a + k, b + l))):
                break
            if(element != Element.HEAT):
                possibilities[a + k][b +
                                     l]["nonpossibilities"].append(Element.FIRE)
            if(element != Element.CRIES):
                possibilities[a + k][b +
                                     l]["nonpossibilities"].append(Element.VICTIM)
            if(element != Element.DIRT):
                possibilities[a + k][b +
                                     l]["nonpossibilities"].append(Element.RUBBLE)
