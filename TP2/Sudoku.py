import random
from datetime import datetime
from CSP import CSP

class Sudoku:
    
    def __init__(self, board, indices):
        """
        Constructeur de la classe Sudoku
        """
        self.size = 9
        self.indices = indices
        random.seed(datetime.now())
        self.grid = self.random_valid_board() if board is None else self.load_board(board)
        self.csp = CSP(self.size)
        self.csp.update_domains(self.grid)
    
    def random_valid_board(self):
        """
        Génère un sudoku aléatoire et valide
        """
        #chargement de la table de base
        board = self.load_board("BASE_SUDOKU.txt")
        
        #rotation aléatoire du sudoku
        for i in range(0, random.randint(0, 3)):
            board = [list(reversed(col)) for col in zip(*board)]
        available_variables = [i for i in range(1, 10)]
        
        #échange aléatoire des chiffres
        for m in range(random.randint(5, 15)):
            t_num1 = available_variables[random.randint(0, len(available_variables) - 1)]
            t_num2 = available_variables[random.randint(0, len(available_variables) - 1)]
            while t_num2 == t_num1:
                t_num2 = available_variables[random.randint(0, len(available_variables) - 1)]
            
            for k in range(len(board)):
                board[k] = [i if i != t_num1 and i != t_num2 else t_num1 if i == t_num2 else t_num2 for i in board[k]] 

        #suppression de quelques cases pour générer un sudoku valide
        for _ in range(self.size**2 - self.indices):
            r = random.randint(0, self.size**2 - 1)
            while board[r // self.size][r % self.size] == 0:
                r = random.randint(0, self.size**2 - 1)
            board[r // self.size][r % self.size] = 0
            
        return board
    
    def load_board(self, board):
        """
        Charge un sudoku dans la grille à partir d'un fichier
        """
        with open(board, "r") as f:
            lines = f.readlines()
        return [[int(x) for x in line.strip()] for line in lines]
    
    def count_non_empty_cells(self):
        """
        Compte le nombre de cases non vides
        """
        return sum(1 for row in self.grid for el in row if el != 0)
        
    def complete_sudoku(self, new_csp):
        """
        Remplit le sudoku avec les valeurs trouvées dans le CSP
        """
        for var in new_csp.variables:
            if len(new_csp.domains[var]) == 1:
                self.grid[var // self.size][var % self.size] = new_csp.domains[var][0]
                self.csp.domains[var] = [0]
        return self.grid
        
    def __repr__(self):
        """
        Fonction de représentation du sudoku, utilisée avec print(sudoku)
        """
        tmp_string = ""
        for i in range(self.size + 4):
            tmp_string += "- "
        tmp_string += "-\n"
        count = 0
        for row in self.grid:
            count += 1
            tmp_string += " ".join(str(el) + " " if el != 0 else "  " for el in row[0:3]) + "| " + " ".join(str(el) + " " if el != 0 else "  " for el in row[3:6]) + "| " + " ".join(str(el) + " " if el != 0 else "  " for el in row[6:9]) + "\n"
            if(count == 3):
                count = 0
                for i in range(len(row) + 4):
                    tmp_string += "- "
                tmp_string += "-\n"
            
        return tmp_string
    
    def verify(self):
        """
        Vérifie si le sudoku est valide
        """
        return self.verify_completed() and self.verify_rows() and self.verify_cols() and self.verify_boxes()
    
    def verify_completed(self):
        """
        Vérifie si le sudoku est complet
        """
        return self.count_non_empty_cells() == self.size ** 2
    
    def verify_rows(self):
        """
        Vérifie si les lignes du sudoku sont valides (pas de doublon de chiffre)
        """
        for row in self.grid:
            if len(set(row)) != self.size:
                return False
        return True
    
    def verify_cols(self):
        """
        Vérifie si les colonnes du sudoku sont valides (pas de doublon de chiffre)
        """
        for i in range(self.size):
            if len(set(self.grid[i])) != self.size:
                return False
        return True
    
    def verify_boxes(self):
        """
        Vérifie si les boîtes de 3x3 cases du sudoku sont valides (pas de doublon de chiffre)
        """
        for i in range(3):
            for j in range(3):
                a = self.grid[i*3][j*3:j*3+3]
                b = self.grid[i*3+1][j*3:j*3+3]
                c = self.grid[i*3+2][j*3:j*3+3]
                if len(set(a + b + c)) != self.size:
                    return False
        return True
