class Backtracking:
    def __init__(self, csp):
        """
        Constructeur de la classe Backtracking
        """
        self.csp = csp
    
    def run(self):
        """
        Retourne une solution au problème CSP en utilisant la méthode de Backtracking. Renvoie un dictionnaire des domaines pour chaque variable
        """
        print("[Backtracking] Backtracking en cours...\n")
        r = self.recursive_backtracking({})
        r = {i: [r[i]] for i in r}
        self.csp.domains = r
        return self.csp
    
    def recursive_backtracking(self, assignment):
        """
        Fonction récursive appellée pour la méthode de Backtracking
        """
        if self.is_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.get_domain(var):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.recursive_backtracking(assignment)
                if result is not None:
                    return result
                assignment.pop(var)
        return None
    
    def is_complete(self, assignment):
        """
        Retourne True si l'assignement est complet, False sinon
        """
        return len(assignment) == len(self.csp.variables)
    
    def select_unassigned_variable(self, assignment):
        """
        Retourne la première variable non assignée dans l'assignement
        """
        return list(self.csp.variables - assignment.keys())[0]
            
    def get_domain(self, var):
        """
        Retourne la liste des valeurs de la variable var
        """
        return self.csp.domains[var]
    
    def is_consistent(self, var, value, assignment):
        """
        Retourne True si la valeur value pour var respecte les contraintes, False sinon
        """
        couples = self.get_constraints_with_var(var, assignment)
        for couple in couples:
            contrainte = self.csp.constraints[couple]
            nv = self.get_assignement_value(couple[1] if couple[0] == var else couple[0], assignment)
            if not contrainte(value, nv):
                return False
        return True
    
    def get_assignement_value(self, var, assignment):
        """
        Retourne la valeur assignée à la variable var
        """
        return assignment[var]
    
    def get_constraints_with_var(self, var, assignement):
        """
        Retourne la liste des couples de contraintes qui contiennent la variable var
        """
        return [i for i in self.csp.constraints if i[0] == var and i[1] in assignement or i[1] == var and i[0] in assignement]
