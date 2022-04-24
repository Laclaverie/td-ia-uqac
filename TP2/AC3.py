
class AC3:
    def __init__(self, csp):
        """
        Constructeur de la classe AC3
        """
        self.csp = csp
        self.domains = csp.domains.copy()
        self.queue = self.get_all_arcs()
        
    def get_all_arcs(self):
        """
        Retourne la liste des arcs du problème CSP
        """
        tmp = set([])
        for constraint in self.csp.constraints:
            i = constraint[0]
            j = constraint[1]
            if i != j:
                tmp.add((i, j))
        return list(tmp)
    
    def get_domain(self, X):
        """
        Retourne la liste des valeurs possibles (domaine) de la variable X
        """
        return self.domains[X]
    
    def is_consistent(self, Xi, Xj, x):
        """
        Retourne True si la valeur x pour Xi respecte les contraintes avec Xj, False sinon
        """
        contrainte = self.csp.constraints[(Xi, Xj)]
        for y in self.get_domain(Xj):
            if contrainte(y, x):
                return True
        return False
    
    def remove_value(self, X, c):
        """
        Retire la valeur c de la liste des valeurs possibles (domaine) de la variable X
        """
        self.domains.get(X).remove(c)
        
    def get_neighbors(self, X):
        """
        Retourne la liste des variables voisines de X, donc les variables avec lesquelles X est lié par un arc
        """
        tmp = [i for i in self.csp.constraints if i[0] == X or i[1] == X]
        return [i[0] if i[0] != X else i[1] for i in tmp]
    
    def run(self):
        """
        Exécute l'algorithme AC3 et détermine un nouveau dictionnaire de domaines pour le problème CSP. Renvoie un CSP
        """
        def remove_inconsistent_values(Xi, Xj):
            """
            Retire les valeurs de Xi qui ne respectent pas les contraintes avec Xj
            """
            removed = False
            D = self.get_domain(Xi)
            for c in D:
                if not self.is_consistent(Xi, Xj, c):
                    self.remove_value(Xi, c)
                    removed = True
            return removed  

        print("[AC3] AC3 en cours...\n")
        while len(self.queue) > 0:
            p = self.queue.pop()
            Xi = p[0]
            Xj = p[1]
            if remove_inconsistent_values(Xi, Xj):
                D = self.get_domain(Xi)
                if (len(D) < 1):
                    break
                else:
                    for Xk in self.get_neighbors(Xi):
                        self.queue.append((Xk, Xi))

        self.csp.domains = self.domains.copy()
        
        return self.csp
