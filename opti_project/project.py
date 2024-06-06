# construire des solutions valide
# est ce que la solution est élementaire?
# écrire résultat dans un fichier

# résultat = au temps d'allumage total du réseau ? ou au tps d'allumage de chaque capteur

# calculer le temps d'execution
# fonction "glpk" qui callcul le résultat du programme linéaire

#méthode qui enlève les doublons de solution élémentaire (pas obliG je ccrois) 

import itertools
import time
import numpy as np
import os

class Capteur:
    def __init__(self, id, duree_vie, zones):
        self.id = id
        self.duree_vie = duree_vie
        self.zones = zones

    def __str__(self):
        return "Capteur " + str(self.id) + " : duree_vie = " + str(self.duree_vie) + ", zones = " + str(self.zones)
    
    

"""Permet de lire un fichier
:param lien_fichier: lien du fichier à lire
:returns: le nombre de zones, tableau de capteurs
"""
def lire_fichier(lien_fichier):
    # Ouverture du fichier
    fichier = open(lien_fichier)
    # Lecture des premières lignes pour récupérer les informations
    nb_capteurs = int(fichier.readline())
    nb_zones = int(fichier.readline())

    tab_capteur = []
    # Récupération des informations sur la durée de vie des capteurs
    duree_vie_capteurs = fichier.readline().strip().split(" ")
    # Boucle sur tous les capteurs pour récupérer les zones associées
    ligne = fichier.readline()
    for i in range(nb_capteurs):
        zones = ligne.strip().split(" ")
        # Création du capteur et ajout dans le tableau
        tab_capteur.append(Capteur(i+1,duree_vie_capteurs[i], zones))
        ligne = fichier.readline()

    return nb_zones, tab_capteur


"""Génère une/l'ensemble combinaison de capteur qui couvre toute la zone
:param nb_zones: 
:param tab_capteurs: 
:returns: tableau de tableau de capteurs qui permet de couvrir toutes les zones
"""
def generer_combinaison_solution(nb_zones, tab_capteurs, timer_depart, timer_limit): #initiale
    combinaisons = []
    total = 0
    for i in range(1,nb_zones+1):
        for combi in itertools.combinations(tab_capteurs, i):
            # total+= is_valide(combi, nb_zones)
            if is_valide(combi, nb_zones):
                if(is_elementaire(combi,nb_zones)):
                    combinaisons.append(combi)
            current_time = time.process_time()
            if(current_time-timer_depart >= timer_limit):
                print("dans le if de limit timer")
                return combinaisons
    # print(total)
    return combinaisons

# TODO idées heuristiques
# - trier capteurs par nombre de zones couvertes, choisir ceux qui en ont le plus en premier jusqu'à solution
# - trier capteurs par nombre de zones couvertes, choisir ceux qui en ont le moins en premier jusqu'à solution
# - (sélection des capteurs au fur et à mesure en ajoutant les capteurs tant que la solution n'est pas valide, 
    # puis changer de capteur de départ)
# - prendre un ensemble de solution qui regroupe le plus de capteurs et après 
    # limiter cet ensemble grâce à une méthode est élémentaire dans lquelle on enlève un capteur, puis un autre si tjs possible ...

def heuristique_recursion(nb_zones, tab_capteurs, index_current_capteur, current_solution, list_solutions, list_tabou, nb_iterations):
    nb_iterations+=1
    for i in range(index_current_capteur, len(tab_capteurs)): #obtenir une solution
        capteur = tab_capteurs[i]
        # print("for :", capteur)
        if (capteur not in list_tabou):
            list_tabou.append(capteur)
            # print("list_tabou :", list_tabou)
            
            # if pour pas ajouter capteur inutile
            if(not zones_in_list_capteurs(capteur, current_solution)):
                current_solution.append(capteur)
                # print("current_solution :", current_solution)
            
                #Tester si soultion est OK
                if(is_valide(current_solution, nb_zones)):
                    if(is_elementaire(current_solution,nb_zones)):
                        list_solutions.append(current_solution)
                        # print("list_solutions :", list_solutions)
                        # Si liste tabou est remplie (= nombre de capteurs), on la réinitialise
                        if(len(list_tabou) == len(tab_capteurs)):
                            # print("last if : " , current_solution[0].id, list_tabou[:current_solution[0].id])
                            return heuristique_recursion(nb_zones, tab_capteurs, current_solution[0].id, [], list_solutions, list_tabou[:current_solution[0].id], nb_iterations)
                        # print("last else : " , capteur.id -1, list_tabou, current_solution[:-1])
                        return heuristique_recursion(nb_zones, tab_capteurs, capteur.id -1, current_solution[:-1], list_solutions, list_tabou, nb_iterations)

    #condition d'arrêt
    # if(current_solution == []):
    #     return list_solutions
    if(index_current_capteur == len(tab_capteurs)-1):
        return list_solutions
    
    #condition d'arrêt
    # if(nb_iterations == len(tab_capteurs)):
    #     return list_solutions
    
    return heuristique_recursion(nb_zones, tab_capteurs, current_solution[0].id, [], list_solutions, list_tabou[:current_solution[0].id], nb_iterations)


"""Vérifie si les zones couvertes par le capteur sont déjà couvertes par la solution
:param solution :TODO
:param nb_zones :
:returns:
"""
def zones_in_list_capteurs(test_capteur, solution):
    if(test_capteur.zones == []): 
        return False
    zones_couvertes = []
    for capteur in solution:
        zones_couvertes.extend(capteur.zones)
    zones_couvertes = list(set(zones_couvertes))
    return all(zone in zones_couvertes for zone in test_capteur.zones)

#amélioration avec permutations[0][0]
"""Vérifie si la solution est valide
:param solution : tableau de tableau de capteurs
:param nb_zones : nombre de zones
:returns: True si la solution est valide, False sinon
"""
def is_valide(solution, nb_zones):
    start_time = time.process_time()
    zones_couvertes = []
    for capteur in solution:
        zones_couvertes.extend(capteur.zones)
    zones_couvertes = list(set(zones_couvertes))
    if len(zones_couvertes) == nb_zones:
        # end_time = time.process_time()
        # return end_time-start_time
            return True
    # end_time = time.process_time()
    # return end_time-start_time
    return False

"""Vérifie si la solution est élémentaire
:param solution : tableau de tableau de capteurs
:param nb_zones : nombre de zones
:returns: True si la solution est élémentaire, False sinon
"""
def is_elementaire(solution, nb_zones):
    start_time = time.process_time()
    for capteur_test in solution:
        zones_couvertes = []
        for capteur in solution:
            if(capteur_test!=capteur):
                zones_couvertes.extend(capteur.zones)
            zones_couvertes = list(set(zones_couvertes))
            if len(zones_couvertes) == nb_zones:
                # end_time =[0][0] time.process_time()
                # return end_time-start_time
                return False
    # end_time = time.process_time()
    # return end_time-start_time
    return True

"""TODO
:param solutions_elementaires : toutes les solutions qui sont élémentaires
:param tab_capteurs : contient tout les capteurs
:returns: True si la solution est élémentaire, False sinon
"""
def create_data_prog_linear(solutions_elementaires,tab_capteurs):
    system_lineaire = np.zeros((len(tab_capteurs),len(solutions_elementaires))) # Matrice de nb_capteurs lignes et nb_solutions colonnes ne contenant que des 0
    data_linear = ""
    first_line = "Maximize "
    # i = colonne
    for i in range(len(solutions_elementaires)):
        first_line += "t"+ str(i+1) + "+"
        for capteur in solutions_elementaires[i]:
            system_lineaire[capteur.id-1][i] = 1
    data_linear += first_line[:-1] + "\n\nSubject To\n\n"
    for i in range(len(tab_capteurs)):
        line = format_linear_line(system_lineaire[i])
        data_linear += line + " <= " + tab_capteurs[i].duree_vie +"\n"
    return data_linear+"\nEND"


"""TODO
:param solutions_elementaires :
:returns:
"""
def format_linear_line(row):
    line = ""
    for i in range(len(row)):
        if(row[i] != 0):
            line += "t" + str(i+1) + "+"
    return line[:-1]


"""TODO
:param solutions_elementaires :
:returns: le fichier .lp
"""
def create_file_prog_linear(data_linear,nom_fichier):
    nom_fichier = "../results/recursion/"+nom_fichier
    fichier = open(nom_fichier+"_prog.lp","w")
    fichier.write(data_linear)
    fichier.close()
    return nom_fichier


"""Execute le programme linéaire TODO
:param fichier : le fichier contenant le programme linéaire
:param nb_zones : nombre de zones
:returns: True si la solution est élémentaire, False sinon
"""
def execute_prog_linear(nom_fichier):
    os.system('glpsol --cpxlp '+nom_fichier+'_prog.lp -o '+nom_fichier+'_solution')

#Main
# lien_fichier = '../data/fichier-exemple.txt'
# lien_fichier = '../data/moyen_test_2.txt'
# lien_fichier = '../data/moyen_test_3.txt'
lien_fichier = '../data/gros_test_1.txt'
# lien_fichier = '../data/maxi_test_1.txt'

nb_zones, tab_capteurs = lire_fichier(lien_fichier)
# # print(nb_zones)
# # for capteur in tab_capteurs:",current_solution[0].id)
#     # for capt in list_tabou:
#     #     print("liste tabou",capt)
# #     print(capteur)

current_time = time.process_time()
combinaisons = generer_combinaison_solution(nb_zones, tab_capteurs,current_time,60)
# for combi in combinaisons:
#     print("\nSolution : ")
#     for capteurs in combi:
#         print(capteurs)

# combinaisons = heuristique_recursion(nb_zones, tab_capteurs, 0, [], [], [], 0)
# for combi in combinaisons:
#     print("\nSolution : ")
#     for capteurs in combi:
#         print(capteurs)

return_lines = create_data_prog_linear(combinaisons, tab_capteurs)
# nom_fichier = create_file_prog_linear(return_lines,"fichier-exemple")
# nom_fichier = create_file_prog_linear(return_lines,"moyen_test_2")
# nom_fichier = create_file_prog_linear(return_lines,"moyen_test_3")
nom_fichier = create_file_prog_linear(return_lines,"gros_test_1")
# nom_fichier = create_file_prog_linear(return_lines,"maxi_test_1")

execute_prog_linear(nom_fichier)