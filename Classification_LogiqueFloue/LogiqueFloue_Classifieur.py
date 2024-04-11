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
potentiometre = ctrl.Antecedent(np.arange(VALEUR_MIN_POTENTIOMETRE, VALEUR_MAX_POTENTIOMETRE+1, 1), 'potentiometre')
douleur = ctrl.Consequent(np.arange(VALEUR_MIN_DOULEUR, VALEUR_MAX_DOULEUR+1, 0.5), 'douleur')

"""
Assignation des classes
    On va associer à différentes intervalles de valeurs du potentiometre des classes de douleurs.

    Pour cela on utilise une modélisation du potentiometre à l'aide d'une gaussienne ("gaussmf") à laquelle on passe en paramètre :
        @ x : list, l'univers
        @ a : int, le centre de la gaussienne
        @ b : int, une valeur permettant de régler la largeur de la gaussienne

    Pour la modélisation de la douleur, on n'utilise pas une gaussienne mais une fonction trianglulaire ("trimf"),
    car l'intervalle de valeur est trop petit et l'écart entre chaque valeur trop faible pour qu'une courbe gaussienne soit pertinente.
    On utilise les parametres :
        @ x : list, l'univers
        @ abc : list, avec 
            @ a : int, point d'orgine de la courbe sur l'axe X
            @ b : int, point maximal de valeur 1
            @ c : int, point de chute de la courbe sur l'axe X

    Voir la documentation de skfuzzy pour plus de détails : https://pythonhosted.org/scikit-fuzzy/
"""
potentiometre['douleur_0'] = fuzz.gaussmf(potentiometre.universe, VALEUR_MAX_POTENTIOMETRE/20.0, VALEUR_MAX_POTENTIOMETRE/20.0)
potentiometre['douleur_1'] = fuzz.gaussmf(potentiometre.universe, VALEUR_MAX_POTENTIOMETRE/20.0 + VALEUR_MAX_POTENTIOMETRE/10.0, VALEUR_MAX_POTENTIOMETRE/20.0)
potentiometre['douleur_2'] = fuzz.gaussmf(potentiometre.universe, VALEUR_MAX_POTENTIOMETRE/20.0 + 2.0*VALEUR_MAX_POTENTIOMETRE/10.0, VALEUR_MAX_POTENTIOMETRE/20.0)
potentiometre['douleur_3'] = fuzz.gaussmf(potentiometre.universe, VALEUR_MAX_POTENTIOMETRE/20.0 + 3.0*VALEUR_MAX_POTENTIOMETRE/10.0, VALEUR_MAX_POTENTIOMETRE/20.0)
potentiometre['douleur_4'] = fuzz.gaussmf(potentiometre.universe, VALEUR_MAX_POTENTIOMETRE/20.0 + 4.0*VALEUR_MAX_POTENTIOMETRE/10.0, VALEUR_MAX_POTENTIOMETRE/20.0)
potentiometre['douleur_5'] = fuzz.gaussmf(potentiometre.universe, VALEUR_MAX_POTENTIOMETRE/20.0 + 5.0*VALEUR_MAX_POTENTIOMETRE/10.0, VALEUR_MAX_POTENTIOMETRE/20.0)
potentiometre['douleur_6'] = fuzz.gaussmf(potentiometre.universe, VALEUR_MAX_POTENTIOMETRE/20.0 + 6.0*VALEUR_MAX_POTENTIOMETRE/10.0, VALEUR_MAX_POTENTIOMETRE/20.0)
potentiometre['douleur_7'] = fuzz.gaussmf(potentiometre.universe, VALEUR_MAX_POTENTIOMETRE/20.0 + 7.0*VALEUR_MAX_POTENTIOMETRE/10.0, VALEUR_MAX_POTENTIOMETRE/20.0)
potentiometre['douleur_8'] = fuzz.gaussmf(potentiometre.universe, VALEUR_MAX_POTENTIOMETRE/20.0 + 8.0*VALEUR_MAX_POTENTIOMETRE/10.0, VALEUR_MAX_POTENTIOMETRE/20.0)
potentiometre['douleur_9'] = fuzz.gaussmf(potentiometre.universe, VALEUR_MAX_POTENTIOMETRE/20.0 + 9.0*VALEUR_MAX_POTENTIOMETRE/10.0, VALEUR_MAX_POTENTIOMETRE/20.0)

douleur['douleur_0'] = fuzz.trimf(douleur.universe, [-VALEUR_MAX_DOULEUR/20.0, VALEUR_MAX_DOULEUR/20.0, VALEUR_MAX_DOULEUR/10.0])
douleur['douleur_1'] = fuzz.trimf(douleur.universe, [VALEUR_MAX_DOULEUR/20.0, 3.0*VALEUR_MAX_DOULEUR/20.0, 5.0*VALEUR_MAX_DOULEUR/20.0])
douleur['douleur_2'] = fuzz.trimf(douleur.universe, [3.0*VALEUR_MAX_DOULEUR/20.0, 5.0*VALEUR_MAX_DOULEUR/20.0, 7.0*VALEUR_MAX_DOULEUR/20.0])
douleur['douleur_3'] = fuzz.trimf(douleur.universe, [5.0*VALEUR_MAX_DOULEUR/20.0, 7.0*VALEUR_MAX_DOULEUR/20.0, 9.0*VALEUR_MAX_DOULEUR/20.0])
douleur['douleur_4'] = fuzz.trimf(douleur.universe, [7.0*VALEUR_MAX_DOULEUR/20.0, 9.0*VALEUR_MAX_DOULEUR/20.0, 11.0*VALEUR_MAX_DOULEUR/20.0])
douleur['douleur_5'] = fuzz.trimf(douleur.universe, [9.0*VALEUR_MAX_DOULEUR/20.0, 11.0*VALEUR_MAX_DOULEUR/20.0, 13.0*VALEUR_MAX_DOULEUR/20.0])
douleur['douleur_6'] = fuzz.trimf(douleur.universe, [11.0*VALEUR_MAX_DOULEUR/20.0, 13.0*VALEUR_MAX_DOULEUR/20.0, 15.0*VALEUR_MAX_DOULEUR/20.0])
douleur['douleur_7'] = fuzz.trimf(douleur.universe, [13.0*VALEUR_MAX_DOULEUR/20.0, 15.0*VALEUR_MAX_DOULEUR/20.0, 17.0*VALEUR_MAX_DOULEUR/20.0])
douleur['douleur_8'] = fuzz.trimf(douleur.universe, [15.0*VALEUR_MAX_DOULEUR/20.0, 17.0*VALEUR_MAX_DOULEUR/20.0, 19.0*VALEUR_MAX_DOULEUR/20.0])
douleur['douleur_9'] = fuzz.trimf(douleur.universe, [17.0*VALEUR_MAX_DOULEUR/20.0, 19.0*VALEUR_MAX_DOULEUR/20.0, 21.0*VALEUR_MAX_DOULEUR/20.0])

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
rule0 = ctrl.Rule(potentiometre['douleur_0'], douleur['douleur_0'])
rule1 = ctrl.Rule(potentiometre['douleur_1'], douleur['douleur_1'])
rule2 = ctrl.Rule(potentiometre['douleur_2'], douleur['douleur_2'])
rule3 = ctrl.Rule(potentiometre['douleur_3'], douleur['douleur_3'])
rule4 = ctrl.Rule(potentiometre['douleur_4'], douleur['douleur_4'])
rule5 = ctrl.Rule(potentiometre['douleur_5'], douleur['douleur_5'])
rule6 = ctrl.Rule(potentiometre['douleur_6'], douleur['douleur_6'])
rule7 = ctrl.Rule(potentiometre['douleur_7'], douleur['douleur_7'])
rule8 = ctrl.Rule(potentiometre['douleur_8'], douleur['douleur_8'])
rule9 = ctrl.Rule(potentiometre['douleur_9'], douleur['douleur_9'])

douleur_ctrl = ctrl.ControlSystem([rule0, rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
douleur_mesure = ctrl.ControlSystemSimulation(douleur_ctrl)

"""
Affichage des fonctions d'appartenance
    Pour afficher les fonctions d'appartenances du potentiometre et de la douleur, utilisez les commandes suivantes :
        potentiometre.view()
        douleur.view()
"""
#REMOVE THIS #################################################################################################
potentiometre.view()
douleur.view()

"""
Affichage des fonctions de classe calculées
    Ici on effectue simplement un affichage des fonctions calculés qui sont exportés dans le fichier JSON.
    @ x_points : list, liste des coordonnées X de la fonction flotante
    @ y_points : list, liste des coordonnées Y de la fonction flotante
    @ x_points_round : list, liste des coordonnées X de la fonction entière
    @ y_points_round : list, liste des coordonnées Y de la fonction entière
"""
def Affichages(x_points, y_points, x_points_round, y_points_round):
    # Affichage de la fonction
    plt.plot(x_points, y_points, marker='', linestyle='-')
    plt.title('Valeur de la douleur en fonction du relevé du potentiomètre')
    plt.xlabel('Potentimètre')
    plt.ylabel('Relevé de douleur')
    plt.grid(True)
    plt.show()

    # Affichage de la fonction arrondi
    plt.plot(x_points_round, y_points_round, marker='', linestyle='-')
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
    points_list_round = []

    for valeur_potentiometre in range(VALEUR_MIN_POTENTIOMETRE,VALEUR_MAX_POTENTIOMETRE+1):
        douleur_mesure.input['potentiometre'] = valeur_potentiometre
        douleur_mesure.compute()

        points_list.append([valeur_potentiometre, douleur_mesure.output['douleur']])
        points_list_round.append([valeur_potentiometre, int(douleur_mesure.output['douleur'])])

        #REMOVE THIS #################################################################################################
        if(valeur_potentiometre == 84):
            potentiometre.view(sim=douleur_mesure)
            douleur.view(sim=douleur_mesure)
            input()

        """
        Affichage DEBUG
            Pour un affichage de chaque point de la fonction, utilisez la commande suivantes ici :
                print("DEBUG : ",i, " - ", douleur_mesure.output['douleur'])
        """

    x_points = [point[0] for point in points_list]
    y_points = [point[1] for point in points_list]
    x_points_round = [point[0] for point in points_list_round]
    y_points_round = [point[1] for point in points_list_round]

    """
    Affichage des fonctions de classes calculés :
        Affichages(x_points, y_points, x_points_round, y_points_round)
    """
    Affichages(x_points, y_points, x_points_round, y_points_round)
    input()

    donnees = {"classe_douleur": points_list}
    donnees_round = {"classe_douleur_entiere": points_list_round}

    # Écriture des données dans un fichier JSON
    with open("points_list.json", "w") as json_file:
        json.dump(donnees, json_file)
    with open("points_list_round.json", "w") as json_file:
        json.dump(donnees_round, json_file)

exporter_modele()