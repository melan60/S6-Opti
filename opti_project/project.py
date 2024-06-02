# construire des solutions valide
# est ce que la solution est élementaire?
# écrire résultat dans un fichier

# résultat = au temps d'allumage total du réseau ? ou au tps d'allumage de chaque capteur

# calculer le temps d'execution
# fonction "glpk" qui callcul le résultat du programme linéaire

#méthode qui enlève les doublons de solution élémentaire (pas obliG je ccrois) 

import itertools

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
def generer_combinaison_solution(nb_zones, tab_capteurs): #initiale
    combinaisons = []
    for i in range(1,nb_zones+1):
        for combi in itertools.combinations(tab_capteurs, i):
            if is_valide(combi, nb_zones):
                # TODO : ajouter la condition is_elementaire
                combinaisons.append(combi)
    return combinaisons

# TODO idées heuristiques
# - trier capteurs par nombre de zones couvertes, choisir ceux qui en ont le plus en premier jusqu'à solution
# - trier capteurs par nombre de zones couvertes, choisir ceux qui en ont le moins en premier jusqu'à solution
# - (sélection des capteurs au fur et à mesure en ajoutant les capteurs tant que la solution n'est pas valide, puis changer de capteur de départ)

#amélioration avec permutations
"""Vérifie si la solution est valide

:param solution : tableau de tableau de capteurs
:param nb_zones : nombre de zones
:returns: True si la solution est valide, False sinon
"""
def is_valide(solution, nb_zones):
    zones_couvertes = []
    for capteur in solution:
        for zone in capteur.zones:
            if zone not in zones_couvertes:
                zones_couvertes.append(zone)
        if len(zones_couvertes) == nb_zones:
            return True
    return False


"""Vérifie si la solution est élémentaire

:param solution : tableau de tableau de capteurs
:param nb_zones : nombre de zones
:returns: True si la solution est élémentaire, False sinon
"""
def is_elementaire(solution, nb_zones):

    return 0



#Main
lien_fichier = '../data/fichier-exemple.txt'
nb_zones, tab_capteurs = lire_fichier(lien_fichier)
print(nb_zones)
for capteur in tab_capteurs:
    print(capteur)
combinaisons = generer_combinaison_solution(nb_zones, tab_capteurs)
for combi in combinaisons:
    print("\nSolution : ")
    for capteurs in combi:
        print(capteurs)