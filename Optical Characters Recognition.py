# -*- coding: utf-8 -*-
"""
Created on Wed Sep 07 21:28:55 2022

@author: As
"""
# Remarques :
# - Ce code n'est pas le plus optimisé, mais il est suffisamment simple pour illustrer le principe de l'algorithme.
# - On pourrait par exemple récupérer les lettres d'un document texte et les stocker dans une liste.
# - Il a été décidé (totalement arbitrairement) que les lettres bruitées ayant plus de 5 différences avec les autres lettres soient marquées comme non reconnues. 
#   (Sinon, elle est reconnnue comme celle avec qui elle a le moins grand nombre de différences).

# N'hésitez pas à proposer des améliorations et/ou extensions !

# ----------------- LIBRAIRIES -----------------

from random import shuffle
import random
from math import *

# ----------------- LISTES -----------------

N = 5  # nombre de lignes (et de colonnes) d'une forme

N_cell = N * N

# états des cellules du réseau (booléens)
etats = [False for _ in range(N_cell)]

# seuils des cellules du réseau (réels)
seuils = [0.0 for _ in range(N_cell)]

# poids des connexions du réseau (réels)
poids = [[0.5 for _ in range(N_cell)] for _ in range(N_cell)]

exemple_a_reconnaitre = [[True, False, True, False, True],
                         [True, True, False, False, True],
                         [False, False, True, False, True],
                         [True, False, False, True, True],
                         [True, False, False, False, True]]

alphabet = \
    [[[False, True, True, True, False],   # { A }
      [True, False, False, False, True],
      [True, True, True, True, True],
      [True, False, False, False, True],
      [True, False, False, False, True]],
     [[True, True, True, True, False],    # { B }
      [True, False, False, False, True],
      [True, True, True, True, False],
      [True, False, False, False, True],
      [True, True, True, True, False]],
     [[False, True, True, True, True],    # { C }
      [True, False, False, False, False],
      [True, False, False, False, False],
      [True, False, False, False, False],
      [False, True, True, True, True]],
     [[True, True, True, True, False],  # { D }
      [True, False, False, False, True],
      [True, False, False, False, True],
      [True, False, False, False, True],
      [True, True, True, True, False]],
     [[True, True, True, True, True],     # { E }
      [True, False, False, False, False],
      [True, True, True, False, False],
      [True, False, False, False, False],
      [True, True, True, True, True]],
     [[True, True, True, True, True],     # { F }
      [True, False, False, False, False],
      [True, True, True, False, False],
      [True, False, False, False, False],
      [True, False, False, False, False]],
     [[True, True, True, True, True],     # { G }
      [True, False, False, False, False],
      [True, False, False, False, False],
      [True, False, False, False, True],
      [True, True, True, True, True]],
     [[True, False, False, False, True],  # { H }
      [True, False, False, False, True],
      [True, True, True, True, True],
      [True, False, False, False, True],
      [True, False, False, False, True]],
     [[False, False, True, False, False], # { I }
      [False, False, True, False, False],
      [False, False, True, False, False],
      [False, False, True, False, False],
      [False, False, True, False, False]],
     [[False, False, True, True, True],   # { J }
      [False, False, False, True, False],
      [False, False, False, True, False],
      [False, False, False, True, False],
      [True, True, True, True, False]],
     [[True, False, False, False, True],  # { K }
      [True, False, False, True, False],
      [True, True, True, False, False],
      [True, False, False, True, False],
      [True, False, False, False, True]],
     [[True, False, False, False, False], # { L }
      [True, False, False, False, False],
      [True, False, False, False, False],
      [True, False, False, False, False],
      [True, True, True, True, True]],
     [[True, True, False, True, True],    # { N }
      [True, False, True, False, True],
      [True, False, False, False, True],
      [True, False, False, False, True],
      [True, False, False, False, True]],
     [[True, False, False, False, True],  # { M }
      [True, True, False, False, True],
      [True, False, True, False, True],
      [True, False, False, True, True],
      [True, False, False, False, True]],
     [[False, True, True, True, False],   # { O }
      [True, False, False, False, True],
      [True, False, False, False, True],
      [True, False, False, False, True],
      [False, True, True, True, False]],
     [[True, True, True, True, False],    # { P }
      [True, False, False, False, True],
      [True, True, True, True, False],
      [True, False, False, False, False],
      [True, False, False, False, False]],
     [[True, True, True, True, True],     # { Q }
      [True, False, False, False, True],
      [True, False, False, False, True],
      [True, False, False, True, True],
      [True, True, True, True, True]],
     [[True, True, True, True, False],    # { R }
      [True, False, False, False, True],
      [True, True, True, True, False],
      [True, False, False, True, False],
      [True, False, False, False, True]],
     [[False, True, True, True, True],    # { S }
      [True, False, False, False, False],
      [False, True, True, True, False],
      [False, False, False, False, True],
      [True, True, True, True, False]],
     [[True, True, True, True, True],     # { T }
      [False, False, True, False, False],
      [False, False, True, False, False],
      [False, False, True, False, False],
      [False, False, True, False, False]],
     [[True, False, False, False, True],  # { U }
      [True, False, False, False, True],
      [True, False, False, False, True],
      [True, False, False, False, True],
      [False, True, True, True, False]],
     [[True, False, False, False, True],  # { V }
      [True, False, False, False, True],
      [True, False, False, False, True],
      [False, True, False, True, False],
      [False, False, True, False, False]],
     [[True, False, False, False, True],  # { W }
      [True, False, False, False, True],
      [True, False, False, False, True],
      [True, False, True, False, True],
      [False, True, False, True, False]],
     [[True, False, False, False, True],  # { X }
      [False, True, False, True, False],
      [False, False, True, False, False],
      [False, True, False, True, False],
      [True, False, False, False, True]],
     [[True, False, False, False, True],  # { Y }
      [False, True, False, True, False],
      [False, False, True, False, False],
      [False, False, True, False, False],
      [False, False, True, False, False]],
     [[True, True, True, True, True],     # { Z }
      [False, False, False, True, False],
      [False, False, True, False, False],
      [False, True, False, False, False],
      [True, True, True, True, True]]]

# ----------------- FONCTIONS -----------------
# Fonction de Heavyside
f_activation = lambda x: 0 if x < 0 else 1

# Fontion d'affichage
def affiche_lettre(forme):
    for i in range(N):
        for j in range(N):
            if forme[i][j]:
                print("#", end="")
            else:
                print(" ", end="")
        print("\n")

def affiche_forme(forme):
    for v in range(N):
        for w in range(N):
            if forme[v * 5 + w]:
                print("#", end="")
            else:
                print(" ", end="")
        print("\n")

# Initialiser poids diagonale à 0 (quand i = j)
for i in range(N_cell):
    for j in range(N_cell):
        if i == j:
            poids[i][j] = 0

# ----------------- APPRENTISSAGE -----------------
l = 0  # compteur lettre
eps = 0.21  # epsilon pour s'assurer du résultat (et pas juste atteindre pile poil)
seuils2 = seuils[:]
poids2 = poids[:]
allmodif = 0

print ("____________________________________________")
print ("Apprentissage des lettres avec epsilon = ", eps, "\n")

for l in range (26): #pour les 26 lettres 
    etats2 = etats[:]
    print("Lettre à apprendre", chr(l + 65), ":\n")
    affiche_lettre(alphabet[l])
    resp = [] #cellules responsables du s
    modif = 1 #compteur de modifications pour l'activation d'une cellule, on initialise à 1 pour entrer dans la boucle while
    totmodif = 0 #compteur des modifications pour une lettre
    while modif != 0 :
        modif = 0 #on initialise à 0 pour compter

        # Activation
        for i in range(N_cell):
            s = 0
            for j in range(N_cell):
                if etats2[j]:
                    if i != j: #pas la cellule elle-même
                        s += poids2[i][j]
                        resp.append(j)
            s -= seuils2[i]
            #print("Sortie : ", s)
            
            if s >= seuils2[i]:
                etats2[i] = True
            else :
                etats2[i] = False
                
            # Erreur
            n = i // N  # quotient
            p = i % N  # reste

            if etats2[i] != alphabet[l][n][p] :
                E = s - alphabet[l][n][p]
                #print("Erreur : ", E)
    
                # Modifications 
                d = (E + eps) / (len(resp) + 1) #delta de l'erreur
                d = abs(d)
                #print("Distribution de l'erreur (delta) : ", d)
                
                for k in resp:
                    if etats2[i] == True :
                        poids2[i][k] -= d
                    else :
                        poids2[i][k] += d
                
                    poids2[i][24 - k] = poids2[i][k]  # symétrie
    
                #print("Nombre de modifications : ", modif)
                
                # Modification du seuil
                if etats2[i] == True :
                    seuils2[i] += d
                else :
                    seuils2[i] -= d
                
                modif += 1
                totmodif += 1
                allmodif += 1
                resp.clear()
                        
    if modif == 0 :
        print (totmodif, "modifications effectuées.")  
        print ("Apprentissage de la lettre", chr(l + 65), "terminé :\n")
        affiche_forme(etats2)
        print ("--------------------------------------------")

print (l+1, "lettres apprises.")        
print ("\nNombre moyen de modifications : ", allmodif/26) #25.15 pour e=0.15 ; 21.69 pour 0.19 ; 21.30 pour 0.21
 
# ----------------- RECONNAISSANCE -----------------
print ("____________________________________________ \n")

def reconnaitre_lettre (lettre_a_reco) :
    print ("Reconnaissance de la lettre bruitée \n")
    print ("Lettre à reconnaitre : \n")
    affiche_lettre(lettre_a_reco)
    
    min = 25 #compteur nombre différences minimum
    lettre = 0 #compteur lettre avec minimum de différences avec la lettre bruitée
    
    print ("Différences avec les autres lettres : \n")
    for l in range (26) : #compare à chaque lettre de l'alphabet 
        dif = 0 #compteur nombre différences 
        for i in range(N) :
            for j in range(N) :
                if lettre_a_reco[i][j] != alphabet[l][i][j] : #comparaison
                    dif += 1
        print (chr(l + 65), ":", dif, "différences.")
        if dif < min :
            min = dif  #NB : on aurait pu stocker toutes les différences dans une liste et prendre le minimum
            lettre = l

    if min > 5 : 
        print("\nLa lettre ne semble pas être reconnue. Elle est trop éloignée des autres (plus de 5 différences). \nLa lettre dont elle s'approche le plus est le", chr(lettre + 65), "avec", min, "différences entre les deux lettres.\n")            
    else :
        print ("\nLa lettre bruitée semble être un", chr(lettre + 65), "avec seulement", min, "différences entre les deux lettres.\n")                
    print ("--------------------------------------------\n") 
    
# N bruité  
reconnaitre_lettre(exemple_a_reconnaitre)
    
# Autres lettres
print ("-------------Test d'autres lettres bruitées-------------\n") 
G_bruite = [[True, False, True, True, True], 
            [False, False, False, False, False],
            [True, False, False, False, False],
            [True, True, False, False, True],
            [True, True, True, True, True]]  
    
reconnaitre_lettre(G_bruite)

print ("--------------------------------------------\n") 
K_bruite = [[True, False, False, False, False],  
            [True, False, False, True, True],
            [True, True, True, False, False],
            [False, False, False, True, False],
            [True, False, True, False, True]]

reconnaitre_lettre(K_bruite)

print ("--------------------------------------------\n") 
import numpy
import random
test = [[bool(random.choice([True, False])) for _ in range(N)] for _ in range(N)]
print(test)
affiche_lettre(test)
reconnaitre_lettre(test)
