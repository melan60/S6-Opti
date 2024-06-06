import itertools
import time
import numpy as np
import os


"""Classe Capteur
:param id : identifiant du capteur
:param duree_vie : durée de vie du capteur
:param zones : zones couvertes par le capteur
"""
class Capteur:
    def __init__(self, id, duree_vie, zones):
        self.id = id
        self.duree_vie = duree_vie
        self.zones = zones

    def __str__(self):
        return "Capteur " + str(self.id) + " : duree_vie = " + str(self.duree_vie) + ", zones = " + str(self.zones)
    
    

"""Heuristique 1 : Glouton
Génère toutes les combinaisons possibles de capteurs pour couvrir toutes les zones
:param nb_zones: Nombre de zones
:param tab_capteurs: Tableau de capteurs
:returns: tableau de tableau de capteurs qui permet de couvrir toutes les zones
"""
def generer_combinaison_solution(nb_zones, tab_capteurs, timer_depart, timer_limit): #initiale
    combinaisons = []
    for i in range(1,nb_zones+1):
        # Génère toutes les combinaisons de capteurs
        for combi in itertools.combinations(tab_capteurs, i):
            # Si la combinaison est valide
            if is_valide(combi, nb_zones):
                # Si la combinaison est élémentaire
                if(is_elementaire(combi,nb_zones)):
                    combinaisons.append(combi)
            current_time = time.process_time()
            if(current_time-timer_depart >= timer_limit):
                print("Temps limite dépassé")
                return combinaisons
    return combinaisons

"""Heuristique 2 : Récursion
Parcours récursif pour générer toutes les combinaisons possibles de capteurs pour couvrir toutes les zones
:param nb_zones: Nombre de zones
:param tab_capteurs: Tableau de capteurs
:param index_current_capteur: Index du capteur actuel
:param current_solution: Solution actuelle
:param list_solutions: Liste des solutions
:param list_tabou: Liste des capteurs tabous pour la récursion actuelle
:param timer_depart : temps de départ
:param time_limit : temps limite avant arrêt
:param nb_iterations : nombre d'itérations avant arrêt
:returns: tableau de tableau de capteurs qui permet de couvrir toutes les zones
"""
# def heuristique_recursion(nb_zones, tab_capteurs, index_current_capteur, current_solution, list_solutions, list_tabou, timer_depart, time_limit):
def heuristique_recursion(nb_zones, tab_capteurs, index_current_capteur, current_solution, list_solutions, list_tabou, nb_iterations):
    # Condition d'arrêt sur le nombre d'itérations
    nb_iterations+=1
    if(nb_iterations >= 200):
        print("fin nb_iterations")
        return list_solutions
    ## Condition d'arrêt sur le temps
    # current_time = time.process_time()
    # if current_time-timer_depart >= time_limit:
    #     print("Temps limite dépassé")
    #     return list_solutions
    # Parcourt des capteurs de l'index actuel à la fin
    for i in range(index_current_capteur, len(tab_capteurs)):
        capteur = tab_capteurs[i]
        # Si le capteur n'est pas dans la liste tabou
        if (capteur not in list_tabou):
            list_tabou.append(capteur)
            # Si les zones couvertes par le capteur ne sont pas déjà couvertes par la solution
            if(not zones_in_list_capteurs(capteur, current_solution)):
                current_solution.append(capteur)
                # Si la solution est valide
                if(is_valide(current_solution, nb_zones)):
                    # Si la solution est élémentaire
                    if(is_elementaire(current_solution,nb_zones)):
                        list_solutions.append(current_solution)
                        # Si liste tabou est remplie (= nombre de capteurs), on la réinitialise
                        if(len(list_tabou) == len(tab_capteurs)):
                            # current_solution[0].id : pour repartir de l'index du premier capteur, list_tabou[:current_solution[0].id] : pour réinitialiser la liste tabou
                            # return heuristique_recursion(nb_zones, tab_capteurs, current_solution[0].id, [], list_solutions, list_tabou[:current_solution[0].id], timer_depart, time_limit)
                            return heuristique_recursion(nb_zones, tab_capteurs, current_solution[0].id, [], list_solutions, list_tabou[:current_solution[0].id], nb_iterations)
                        # return heuristique_recursion(nb_zones, tab_capteurs, capteur.id -1, current_solution[:-1], list_solutions, list_tabou, timer_depart, time_limit)
                        return heuristique_recursion(nb_zones, tab_capteurs, capteur.id -1, current_solution[:-1], list_solutions, list_tabou, nb_iterations)

    # Condition d'arrêt normale
    if(index_current_capteur == len(tab_capteurs)-1):
        return list_solutions
    # return heuristique_recursion(nb_zones, tab_capteurs, current_solution[0].id, [], list_solutions, list_tabou[:current_solution[0].id], timer_depart, time_limit)
    return heuristique_recursion(nb_zones, tab_capteurs, current_solution[0].id, [], list_solutions, list_tabou[:current_solution[0].id], nb_iterations)

#=======================================================================================================
#MÉTHODES UTILES
#=======================================================================================================
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


"""Vérifie si les zones couvertes par le capteur sont déjà couvertes par la solution
:param test_capteur : capteur à tester
:param solution : tableau de capteurs
:returns: True si les zones sont déjà couvertes, False sinon
"""
def zones_in_list_capteurs(test_capteur, solution):
    # Si le capteur n'a pas de zones couvertes
    if(test_capteur.zones == []): 
        return False
    zones_couvertes = []
    # Récupération des zones couvertes par les capteurs de la solution
    for capteur in solution:
        zones_couvertes.extend(capteur.zones)
    zones_couvertes = list(set(zones_couvertes))
    # Vérification si toutes les zones du capteur sont dans les zones couvertes
    return all(zone in zones_couvertes for zone in test_capteur.zones)


"""Vérifie si la solution est valide
:param solution : tableau de tableau de capteurs
:param nb_zones : nombre de zones
:returns: True si la solution est valide, False sinon
"""
def is_valide(solution, nb_zones):
    zones_couvertes = []
    for capteur in solution:
        zones_couvertes.extend(capteur.zones)
    zones_couvertes = list(set(zones_couvertes))
    if len(zones_couvertes) == nb_zones:
        return True
    return False

"""Vérifie si la solution est élémentaire
:param solution : tableau de tableau de capteurs
:param nb_zones : nombre de zones
:returns: True si la solution est élémentaire, False sinon
"""
def is_elementaire(solution, nb_zones):
    for capteur_test in solution:
        zones_couvertes = []
        for capteur in solution:
            if(capteur_test!=capteur):
                zones_couvertes.extend(capteur.zones)
            zones_couvertes = list(set(zones_couvertes))
            if len(zones_couvertes) == nb_zones:
                return False
    return True


#=======================================================================================================
#PROGRAMME LINEAIRE
#=======================================================================================================
"""Crée les données pour le programme linéaire
:param solutions_elementaires : toutes les solutions élémentaires
:param tab_capteurs : tableau des capteurs
:returns: les données formatées pour le programme linéaire
"""
def create_data_prog_linear(solutions_elementaires,tab_capteurs):
    # Création de la matrice du système linéaire (nb_capteurs lignes et nb_solutions colonnes)
    system_lineaire = np.zeros((len(tab_capteurs),len(solutions_elementaires)))
    data_linear = ""
    first_line = "Maximize "
    # Parcours des solutions élémentaires pour les ajouter dans la fonction objectif
    for i in range(len(solutions_elementaires)):
        first_line += "t"+ str(i+1) + "+"
        for capteur in solutions_elementaires[i]:
            system_lineaire[capteur.id-1][i] = 1
    data_linear += first_line[:-1] + "\n\nSubject To\n\n"
    # Parcours des capteurs pour les ajouter dans les contraintes
    for i in range(len(tab_capteurs)):
        if system_lineaire[i].sum() != 0:
            line = format_linear_line(system_lineaire[i])
            data_linear += line + " <= " + tab_capteurs[i].duree_vie +"\n"
    return data_linear+"\nEND"


"""Renvoit la ligne formatée pour le programme linéaire
:param row : ligne de la matrice du système linéaire
:returns: la ligne formatée
"""
def format_linear_line(row):
    line = ""
    for i in range(len(row)):
        if(row[i] != 0):
            line += "t" + str(i+1) + "+"
    return line[:-1]


"""Crée le fichier .lp pour le programme linéaire
:param data_linear : données formatées pour le programme linéaire
:param nom_fichier : nom du fichier
:param dossier : dossier de sauvegarde
:returns: le fichier .lp
"""
def create_file_prog_linear(data_linear,nom_fichier,dossier):
    nom_fichier = "../results/"+dossier+"/"+nom_fichier
    fichier = open(nom_fichier+"_prog.lp","w")
    fichier.write(data_linear)
    fichier.close()
    return nom_fichier


"""Execute le programme linéaire et génère le fichier de solution
:param nom_fichier : fichier .lp
"""
def execute_prog_linear(nom_fichier):
    os.system('glpsol --cpxlp ' +nom_fichier+'_prog.lp -o ' +nom_fichier+'_solution > /dev/null 2>&1')


#=======================================================================================================
#=======================================================================================================
def main(liste_fichier):
    for nom_fichier in liste_fichier:
        print("\n",nom_fichier)
        #Lecture du fichier
        nb_zones, tab_capteurs = lire_fichier("../data/"+nom_fichier+".txt")

        #HEURISTIQUE GLOUTON
        current_time_glouton = time.process_time()
        #Générer les configurations élémentaires
        combinaisons_glouton = generer_combinaison_solution(nb_zones, tab_capteurs,current_time_glouton,15)
        return_lines_glouton = create_data_prog_linear(combinaisons_glouton, tab_capteurs)
        fichier = create_file_prog_linear(return_lines_glouton,nom_fichier,"1-glouton")
        execute_prog_linear(fichier)
        end_time_glouton = time.process_time()
        print("\ttps glouton : ", end_time_glouton-current_time_glouton)

        #HEURISTIQUE récursif classique
        current_time_recursif_classique = time.process_time()
        combinaisons_rec_classique = heuristique_recursion(nb_zones, tab_capteurs, 0, [], [], [], 0)
        return_lines_rec_classique = create_data_prog_linear(combinaisons_rec_classique, tab_capteurs)
        fichier = create_file_prog_linear(return_lines_rec_classique,nom_fichier,"2-recursion_classique")
        execute_prog_linear(fichier)
        end_time_recursif_classique = time.process_time()
        print("\ttps rec classique : ", end_time_recursif_classique-current_time_recursif_classique)

        #HEURISTIQUE récursif tri croissant nb_zone / capteurs
        current_time_recursif_croissant = time.process_time()
        # Tri de tab_capteurs par nombre de zones couvertes
        tab_capteurs_croissant = sorted(tab_capteurs, key=lambda x: len(x.zones), reverse=False)
        # Changer l'id des capteurs pour les retrouver
        for i in range(len(tab_capteurs_croissant)):
            tab_capteurs_croissant[i].id = i+1
        combinaisons_rec_croissant = heuristique_recursion(nb_zones, tab_capteurs_croissant, 0, [], [], [], 0)
        return_lines_rec_croissant = create_data_prog_linear(combinaisons_rec_croissant, tab_capteurs_croissant)
        fichier = create_file_prog_linear(return_lines_rec_croissant,nom_fichier,"3-recursion_croissante")
        execute_prog_linear(fichier)
        end_time_recursif_croissant = time.process_time()
        print("\ttps rec croissant : ", end_time_recursif_croissant-current_time_recursif_croissant)

        #HEURISTIQUE récursif tri décroissant nb_zone / capteurs
        current_time_recursif_decroissant = time.process_time()
        # Tri de tab_capteurs par nombre de zones couvertes
        tab_capteurs_decroissant = sorted(tab_capteurs,key=lambda x: len(x.zones), reverse=True)
        # Changer l'id des capteurs pour les retrouver
        for i in range(len(tab_capteurs_decroissant)):
            tab_capteurs_decroissant[i].id = i+1
        combinaisons_rec_decroissant = heuristique_recursion(nb_zones, tab_capteurs_decroissant, 0, [], [], [], 0)
        # combinaisons_rec_decroissant = heuristique_recursion(nb_zones, tab_capteurs_decroissant, 0, [], [], [], 0, 2.5)
        return_lines_rec_decroissant = create_data_prog_linear(combinaisons_rec_decroissant, tab_capteurs_decroissant)
        fichier = create_file_prog_linear(return_lines_rec_decroissant,nom_fichier,"4-recursion_decroissante")
        execute_prog_linear(fichier)
        end_time_recursif_decroissant = time.process_time()
        print("\ttps rec decroissant : ", end_time_recursif_decroissant-current_time_recursif_decroissant)
    return

#=======================================================================================================
                                #EXECUTION DU MAIN
#=======================================================================================================
liste_fichier = ['fichier-exemple','moyen_test_3','moyen_test_2','gros_test_1','maxi_test_1']
main(liste_fichier)