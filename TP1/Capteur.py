from Environnement import Element
class Capteur():
    def __init__(self, environnement):
        self.environnement = environnement

    def isGoal(self, i, j):
        """verifie si la case etudiee contient qq chose d'intéressant"""
        if(Element.JEWEL in self.environnement.map[i][j]["contents"] or Element.DIRT in self.environnement.map[i][j]["contents"]):
            return True
        return False

    def isInBornes(self, position):
        """verifie que la position etudiee est bien dans l'environnement"""
        return position[0] >= 0 and position[0] < self.environnement.taille and position[1] >= 0 and position[1] < self.environnement.taille

    def observe_environnement(self):
        """returns a list of all the positions in the environnement with dirt or jewels"""
        positions = []
        for i in range(self.environnement.taille):
            for j in range(self.environnement.taille):
                if(self.isGoal(i, j)):
                    positions.append((i, j))
        return positions

    def getNeighbors(self, position):
        """renvoie les voisins de la case etudiee"""
        neighbors = []
        #pas bon
        for p in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            i = p[0]
            j = p[1]
            new_position = (position[0] + i, position[1] + j)
            if(self.isInBornes(new_position)):
                neighbors.append({"position": new_position, "weight":self.environnement.map[new_position[0]][new_position[1]]["weight"]})
        return neighbors
