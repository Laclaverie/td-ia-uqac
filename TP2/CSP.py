class CSP:
    def __init__(self, size):
        """
        Constructeur de la classe CSP
        """
        self.variables = [i for i in range(size ** 2)]
        self.domain = [i for i in range(1, size + 1)]
        self.size = size
        self.domains = {}
        for var in self.variables:
            self.domains[var] = self.domain.copy()
            
        constraints = {}
        #remplissage du dictionnaire de contraintes avec des fonctions lambda
        for a in range(size**2):
            for b in range(size**2):
                if a != b and (self.same_row(a, b) or self.same_col(a, b) or self.same_box(a, b)):
                    constraints[(a, b)] = lambda x, y: x != y
                    constraints[(b, a)] = lambda x, y: x != y
        self.constraints = constraints
        
    def update_domains(self, grid):
        """
        Met à jour les domaines des variables
        """
        for i in range(self.size):
            for j in range(self.size):
                if grid[i][j] != 0:
                    self.domains[i * self.size + j] = [grid[i][j]]

    def same_row(self, a, b):
        """
        Retourne True si les deux variables sont dans la même ligne
        """
        return a // self.size == b // self.size
    
    def same_col(self, a, b):
        """
        Renvoie True si les deux variables sont dans la même colonne
        """
        return a % self.size == b % self.size
    
    def same_box(self, a, b):
        """
        Renvoie True si les deux variables sont dans la même boite de 3x3 cases
        """
        return (a // self.size) // 3 == (b // self.size) // 3 and (a % self.size) // 3 == (b % self.size) // 3
