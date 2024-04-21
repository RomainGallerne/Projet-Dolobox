import json
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl

"""
Paramètrage

    - Paramètres du potentiomètre, ceux-ci doivent être en accord avec les valeurs numériques
    qui seront appliquez en entrée de la fonction de classification de la douleur

    - Paramètres de la douleur, ceux-ci doivent représenter les valeurs acceptés par le système de stockage
    qui accueil les données du boîtier.
    ! CE SERONT LES DONNES QUI SERONT EXPORTES !
"""
VALEUR_MIN_POTENTIOMETRE = 0
VALEUR_MAX_POTENTIOMETRE = 200
VALEUR_MIN_DOULEUR = 0
VALEUR_MAX_DOULEUR = 10

"""
Définition des paramètres d'entrée et de sortie.
    - potentiometre est la variable d'entrée du programme, celle-ci s'étale de @valeurMinimale à @ValeurMaximale du slider physique.
    Cette valeur du potentiomètre est analogique et converti numériquement par un autre processus, on suppose ici récupérer directement la valeur numérique, sur le domaine du potentiometre.

    - douleur est la variable de sortie qu'on cherche à calculer, on définit son espace sur l'intervalle [0,10].
"""
potentiometre = ctrl.Antecedent(
    np.arange(
        VALEUR_MIN_POTENTIOMETRE - 20, 
        VALEUR_MAX_POTENTIOMETRE + 1, 
        1
    ),
    'potentiometre'
)

douleur = ctrl.Consequent(
    np.arange(
        VALEUR_MIN_DOULEUR - 1, 
        VALEUR_MAX_DOULEUR + 1, 
        0.1
    ),
    'douleur'
)

"""
Assignation des classes
    On va associer à différentes intervalles de valeurs du potentiometre des classes de douleurs.

    Pour cela on utilise une modélisation du potentiometre à l'aide d'une gaussienne ("gaussmf") à laquelle on passe en paramètre :
        @ x : list, l'univers
        @ a : int, le centre de la gaussienne
        @ b : int, une valeur permettant de régler la largeur de la gaussienne

    Pour la modélisation de la douleur, on n'utilise pas une gaussienne mais une fonction trianglulaire ("trapmf"),
    car l'intervalle de valeur est trop petit et l'écart entre chaque valeur trop faible pour qu'une courbe gaussienne soit pertinente.
    On utilise les parametres :
        @ x : list, l'univers
        @ abcd : list, avec 
            @ a : int, point d'orgine de la courbe sur l'axe X
            @ b : int, premier point maximal de valeur 
            @ b : int, second point maximal de valeur 
            @ d : int, point de chute de la courbe sur l'axe X

    Voir la documentation de skfuzzy pour plus de détails : https://pythonhosted.org/scikit-fuzzy/
"""

for classe_douleur in range(VALEUR_MIN_DOULEUR,VALEUR_MAX_DOULEUR + 1):

    potentiometre['douleur_'+str(classe_douleur)] = fuzz.gaussmf(
        potentiometre.universe, 
        (VALEUR_MAX_POTENTIOMETRE / VALEUR_MAX_DOULEUR) * classe_douleur, 
        VALEUR_MAX_POTENTIOMETRE / (3.0 * VALEUR_MAX_DOULEUR)
    )
    
    douleur['douleur_'+str(classe_douleur)] = fuzz.gaussmf(
        douleur.universe, 
        classe_douleur,
        0.5
    )
"""
Affichage des fonctions d'appartenance
    Pour afficher les fonctions d'appartenances du potentiometre et de la douleur, utilisez les commandes suivantes :
        potentiometre.view()
        douleur.view()
"""
print("INFO : Affichage des classes potentiometre et douleur.")
potentiometre.view()
douleur.view()
input()

"""
Règles Logiques
    Ici, on définit les régles logiques qui permettent les inférences du système de logique floues.
    "ctrl.Rule" permet de définir une nouvelle règle et prends les paramètres :
        @ x : une classe d'une valeur d'entrée, ici le potentiomètre
        @ y : une classe de la valeur de sortie, ici la douleur

    On associe donc à chaque classe du potentiomètre une classe correspondante de la douleur,
    celles-ci ont été nommées identiquement pour une meilleure lisibilité du code mais ce n'est pas une obligation.

   Voir la documentation de skfuzzy pour plus de détails : https://pythonhosted.org/scikit-fuzzy/
"""
rules = []
for classe_douleur in range(VALEUR_MIN_DOULEUR,VALEUR_MAX_DOULEUR + 1):

    rule = ctrl.Rule(
        potentiometre['douleur_'+str(classe_douleur)], 
        douleur['douleur_'+str(classe_douleur)]
    )

    rules.append(rule)

douleur_ctrl = ctrl.ControlSystem(rules)
douleur_mesure = ctrl.ControlSystemSimulation(douleur_ctrl)
douleur_mesure.defuzzify_method = 'centroid'


"""
Affichage des fonctions de classe calculées
    Ici on effectue simplement un affichage des fonctions calculés qui sont exportés dans le fichier JSON.
    @ x_points : list, liste des coordonnées X de la fonction flotante
    @ y_points : list, liste des coordonnées Y de la fonction flotante
    @ x_points_round : list, liste des coordonnées X de la fonction entière
    @ y_points_round : list, liste des coordonnées Y de la fonction entière
"""
def Affichages(y_points, y_points_round):
    # Affichage de la fonction
    X_points = [X for X in range(VALEUR_MIN_POTENTIOMETRE, VALEUR_MAX_POTENTIOMETRE+1)]
    plt.plot(X_points, y_points, marker='', linestyle='-')
    plt.title('Valeur de la douleur en fonction du relevé du potentiomètre')
    plt.xlabel('Potentimètre')
    plt.ylabel('Relevé de douleur')
    plt.grid(True)
    plt.show()

    # Affichage de la fonction arrondi
    plt.plot(X_points, y_points_round, marker='', linestyle='-')
    plt.title('Valeur de la douleur arrondi en fonction du relevé du potentiomètre')
    plt.xlabel('Potentimètre')
    plt.ylabel('Relevé de douleur arrondi')
    plt.grid(True)
    plt.show()

"""
Fonction d'export du modèle
    Afin de ne pas avoir à faire tourner tout le modèle de logique flou à chaque calcul, on l'exporte sous la forme d'une fonction au format JSON.
    On créer deux fichiers JSON en sortie :
        - points_list.json, ce fichier contient une fonction dont les valeurs sont 
            @ X : [0,200], les valeurs entières du potentiomètres
            @ Y : [0.0,10.0], les valeurs flotantes de la douleur
        - points_list_round.json, ce fichier contient une fonction dont les valeurs sont 
            @ X : [0,200], les valeurs entières du potentiomètres
            @ Y : [0,10], les valeurs entières de la douleur

    Pour un enregistrement dans le DPI, la fonction points_list_round est à privilégier.
"""
def exporter_modele():
    points_list = []
    points_list_dixieme = []

    for valeur_potentiometre in range(VALEUR_MIN_POTENTIOMETRE,VALEUR_MAX_POTENTIOMETRE+1):
        douleur_mesure.input['potentiometre'] = valeur_potentiometre
        douleur_mesure.compute()

        points_list.append([valeur_potentiometre, douleur_mesure.output['douleur']])
        points_list_dixieme.append([valeur_potentiometre, round(douleur_mesure.output['douleur'], 1)])

        #RETIRER CETTE CONDITIONNELLE POUR SUPPRIMER L AFFICHAGE DEBUG#
        if(valeur_potentiometre == 84):
            print("INFO : Affichage des courbes pour l'entrée 84.")
            potentiometre.view(sim=douleur_mesure)
            douleur.view(sim=douleur_mesure)
            input()
        """
        Affichage DEBUG
            Pour un affichage de chaque point de la fonction, utilisez la commande suivantes ici :
                print("DEBUG : ",i, " - ", douleur_mesure.output['douleur'])
        """

    y_points = [point[1] for point in points_list]
    y_points_round = [point[1] for point in points_list_dixieme]

    """
    Affichage des fonctions de classes calculés :
        Affichages(x_points, y_points, x_points_round, y_points_round)
    """
    Affichages(y_points, y_points_round)
    input()

    donnees = {"classe_douleur": y_points}
    donnees_dixieme = {"classe_douleur_entiere": y_points_round}

    """
    Fonction d'export au format JSON
    """
    with open("points_list.json", "w") as json_file:
        json.dump(donnees, json_file)
    with open("points_list_dixieme.json", "w") as json_file:
        json.dump(donnees_dixieme, json_file)

exporter_modele()