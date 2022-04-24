from audioop import reverse
import threading
from anytree import AnyNode
from enum import IntEnum
import Settings
import datetime

class Algo(IntEnum):
    BFS = 0
    ASTAR = 1
    
class Agent():
    def __init__(self, capteur, effecteur, want_uninformed_only):
        self.alive = False
        self.capteur = capteur
        self.effecteur = effecteur
        nb_cases = self.capteur.environnement.taille**2
        self.metric = [[{"poids":10000, "chemin":[]} for i in range(nb_cases)] for j in range(nb_cases)] #matrice d'adjacence des chemins de poids le plus bas trouvés pendant l'exploration 
        self.thread = None
        self.want_uninformed_only = want_uninformed_only
        self.initial_counter_metric = ((nb_cases)**2 - nb_cases) /2 + nb_cases
        self.counter_metric = self.initial_counter_metric
        self.goals = []
        
    def start_thread(self):
        """start agent thread""" 
        self.alive = True
        self.thread = threading.Thread(target=self.run_agent)
        self.thread.start()
        
    def stop_thread(self):
        """stop agent thread"""
        self.alive = False
        self.thread.join()
        print("[Console] - Thread de l'agent arrêté")
    
    def run_agent(self):
        """boucle principale d'execution de l'agent"""
        
        def apprentissage_fini():
            return not self.want_uninformed_only and self.counter_metric == 0
        
        algo = Algo.BFS
        print("[Agent] - Algorithme BFS")
        self.effecteur.move_robot() #move robot to current position
        while self.alive:
            if algo != Algo.ASTAR and apprentissage_fini():
                print("[Agent] - Métrique : " + str(self.metric))
                print("[Agent] - Métrique remplie, je passe en mode informé (Algorithme Astar)")
                algo = Algo.ASTAR
                Settings.globalList[0] = True
            else:
                now = datetime.datetime.now()
                print(str(now.hour) + ":" + (str(now.minute) if now.minute >= 10 else "0" + str(now.minute)) + " | [Agent] - Apprentissage : progression : " + str(int(
                    self.initial_counter_metric - self.counter_metric)) + "/" + str(int(self.initial_counter_metric)), flush=True)
            if algo == Algo.ASTAR:
                self.goals = self.capteur.observe_environnement()
            chemin = self.execute_exploration(algo) #construction de l'arbre d'exploration
            if len(chemin) > 0:
                if Settings.globalList[0]:
                    print("[Agent] - Chemin trouvé : " + str(chemin))
                self.metric = self.execute_action_plan(chemin) #met à jour la métrique et la position du robot
            
    def execute_exploration(self, algo):
        """construit le plan local d'exploration"""
        
        def get_closest_goal(start_point):
            
            def get_other_position_from_mat_metric(j):
                """return the other position from a matric metric"""
                return (j // self.capteur.environnement.taille, j % self.capteur.environnement.taille)
                
            list_goals_weight = []
            start_mat_metric = (start_point[0] * self.capteur.environnement.taille)+(start_point[1])
            line = self.metric[start_mat_metric]
            for goal in self.goals:
                list_goals_weight.append({"goal": goal, "weight":line[(goal[0] * self.capteur.environnement.taille)+(goal[1])]["poids"]})
            min_goal = None
            min_weight = 10000
            for g in list_goals_weight:
                if(g["weight"] < min_weight):
                    min_goal = g["goal"]
                    min_weight = g["weight"]
            
            return min_goal
        
        if algo == Algo.BFS:
            return self.BFS(self.effecteur.position)
        elif algo == Algo.ASTAR:
            start = self.effecteur.position
            goal = get_closest_goal(start)
            return self.Astar(start, goal)
    
    def execute_action_plan(self, action):
        """effectue le plan local d'exploration en mettant à jour la position et la métrique"""
        self.effecteur.update_position(action[-1])
        self.effecteur.move_robot()  # move robot to position
        self.effecteur.decide_what_to_do()
        map_env = self.capteur.environnement.map
        poids_chemin = 0
        for coord in action:
            poids_chemin += map_env[coord[0]][coord[1]]["weight"]
        metric = self.metric
        depart = action[0]
        destination = action[-1]
        dep_mat_metric = (depart[0] * self.capteur.environnement.taille)+(depart[1])
        dest_mat_metric = (destination[0] * self.capteur.environnement.taille)+destination[1]
        if poids_chemin < metric[dep_mat_metric][dest_mat_metric]["poids"]:
            if metric[dep_mat_metric][dest_mat_metric]["poids"] == 10000:
                self.counter_metric -= 1
            metric[dep_mat_metric][dest_mat_metric]["poids"] = poids_chemin
            metric[dest_mat_metric][dep_mat_metric]["poids"] = poids_chemin
            metric[dep_mat_metric][dest_mat_metric]["chemin"] = action
            metric[dest_mat_metric][dep_mat_metric]["chemin"] = action[::-1]
        return metric
    
    def BFS(self, current_agent_position):
        """algorithme BFS basé sur le le pseudo-code"""
        rootNode = AnyNode(id=current_agent_position)
        chemin = []
        lastNode = rootNode
        queue = []
        queue.append(rootNode)
        while len(queue) > 0:
            lastNode = queue.pop(0)
            if self.capteur.isGoal(lastNode.id[0], lastNode.id[1]):
                chemin.append(lastNode.id)
                while lastNode.parent is not None:
                    lastNode = lastNode.parent
                    chemin.append(lastNode.id)
                return chemin[::-1]
            for neighbor_object in self.capteur.getNeighbors([lastNode.id[0], lastNode.id[1]]):
                neighbor_position = neighbor_object["position"]
                if self.capteur.isInBornes(neighbor_position):
                    newNode = AnyNode(id=neighbor_position, parent=lastNode)
                    queue.append(newNode)

        return chemin
    
    def Astar(self, start_pos, goal_pos):
        
        if goal_pos is None:
            return []
        print("[Agent] - Utilisation de l'algorithme ASTAR")

        def reconstruct_path(cameFrom, current):
            total_path = [current]
            while current in cameFrom.keys():
                current = cameFrom[current]
                total_path.insert(0, current)
            return total_path
    
        openSet = [start_pos]
        cameFrom = {}
        gScore = {}
        gScore[start_pos] = 0
        fScore = {}
        start_mat_metric = (start_pos[0] * self.capteur.environnement.taille)+(start_pos[1])
        goal_mat_metric = (goal_pos[0] * self.capteur.environnement.taille)+(goal_pos[1])

        fScore[start_pos] = self.metric[start_mat_metric][goal_mat_metric]["poids"]
        
        while len(openSet) > 0:
            current = min(openSet, key=lambda o: fScore[o])
            if current[0] == goal_pos[0] and current[1] == goal_pos[1]:
                return reconstruct_path(cameFrom, current)

            openSet.remove(current)
            for neighbor_obj in self.capteur.getNeighbors(current):
                tentative_gScore = gScore[current] + int(neighbor_obj["weight"])
                neighbor = neighbor_obj["position"]
                if neighbor not in gScore.keys() or tentative_gScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    neighbor_pos_metric = (neighbor[0] * self.capteur.environnement.taille)+(neighbor[1])
                    goal_pos_metric = (goal_pos[0] * self.capteur.environnement.taille)+(goal_pos[1])
                    fScore[neighbor] = tentative_gScore + self.metric[neighbor_pos_metric][goal_pos_metric]["poids"]
                    if neighbor not in openSet:
                        openSet.append(neighbor)
        return []
