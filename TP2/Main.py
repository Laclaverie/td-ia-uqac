import argparse
from Sudoku import Sudoku
from AC3 import AC3
from Backtracking import Backtracking

def main(args):
    
    sudoku = Sudoku(args.file, min(81, args.indices))
    print("\n[Sudoku] SUDOKU INITIAL\n")
    print(sudoku)
    print("\n--------------------------\n")

    if args.backtracking:
        backtracking = Backtracking(sudoku.csp)
        new_csp = backtracking.run()
    else:
        ac3 = AC3(sudoku.csp)
        new_csp = ac3.run()
    
    new_grid = sudoku.complete_sudoku(new_csp)

    final_message = "SOLUTION TROUVÉE !" if sudoku.verify() else "SUDOKU INSOLVABLE"
    print(f"[Sudoku] {final_message}\n")
    print(sudoku)

    a = input("[Console] Appuyez sur une touche pour quitter")


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='TP2 - Sudoku')

    parser.add_argument('--backtracking', action="store_true", dest="backtracking",
                        default=False, help='Utiliser l\'algorithme de backtracking')
    parser.add_argument('--indices', action="store", dest="indices",
                        type=int, default=45, help='Nombre de premiers chiffres sur la grille à générer')
    parser.add_argument('--file', action="store", dest="file",
                        default=None, help='Fichier contenant le sudoku à charger')
    
    args = parser.parse_args()
    try:
        main(args)
    
    except KeyboardInterrupt:
        print("\n[Console] KeyboardInterrupt - Arret du programme demandé par l'utilisateur. Veuillez patienter...")
    
    print("[Console] Fin du programme...")
