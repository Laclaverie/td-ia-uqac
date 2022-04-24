from Board import Board
# from Capteur import Capteur
# from Effecteur import Effecteur
from Agent import Agent
import time
import argparse
import Settings

def main():
    A = Agent()
    i = 0
    while(True):
        run_level(A, 3 + i)
        i+=1

def run_level(A, size):
    print("Niveau de taille " + str(size))
    B = Board(size)
    print(B)
    try:
        A.run(B)
    except Exception as e:
        print(e)
        exit(1)
    caca = input("Passage au niveau suivant ?")

if __name__ == '__main__':
    main()
