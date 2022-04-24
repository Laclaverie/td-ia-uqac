from Environnement import Environnement
from Capteur import Capteur
from Effecteur import Effecteur
from Agent import Agent
import time
import argparse
import Settings

def main(uninformed, sleep_time, freq_generation, size):
    environnement = Environnement(size, freq_generation)
    capteur = Capteur(environnement)
    effecteur = Effecteur(environnement)
    agent = Agent(capteur, effecteur, uninformed)
    agent.start_thread()
    
    if uninformed:
        try:
            time.sleep(sleep_time)
            agent.stop_thread()
            environnement.stop_thread()
            print("[Console] - Fin du programme")
        except KeyboardInterrupt:
            print("[Console] - Arret du programme demandé par l'utilisateur. Veuillez patienter...")
            agent.stop_thread()
            environnement.stop_thread()
            print("[Console] - KeyboardInterrupt")
    
    else:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("[Console] - Arret du programme demandé par l'utilisateur. Veuillez patienter...")
            agent.stop_thread()
            environnement.stop_thread()
            print("[Console] - KeyboardInterrupt")

    
if __name__ == '__main__':
    Settings.init() 
    
    parser = argparse.ArgumentParser(description='TP1 - Robot-aspirateur')

    parser.add_argument('--size', action="store", dest="size", type=int, default=5, help='Largeur et longueur du manoir (défaut 5)')
    parser.add_argument('--uninformed', action="store_true", default=False, help='Utiliser un algorithme non informé UNIQUEMENT')
    parser.add_argument('--time-limit', action="store", dest="time_limit", type=int, default=120, help='Temps limite d\'exécution du programme non informé UNIQUEMENT en secondes')
    parser.add_argument('--verbose', action="store_true", default=False, help='Détail lors de l\'exécution de l\algorithme non informé pour la création de la métrique')
    parser.add_argument('--gen-interval', action="store", dest="generation_interval", type=float, default=0.05, help='Intervalle de génération des objets en secondes')
    args = parser.parse_args()
    
    Settings.globalList[0] = args.verbose or args.uninformed
    main(args.uninformed, args.time_limit, args.generation_interval, args.size)
