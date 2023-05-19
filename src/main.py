# -*- coding: utf-8 -*-

# Nicolas, 2021-03-05
from __future__ import absolute_import, print_function, unicode_literals

import random 
import numpy as np
import sys
import time
import copy
from itertools import chain


import pygame

from pySpriteWorld.gameclass import Game,check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
from search import probleme

sys.path.append("./Joueur")
from JoueurRandom import JoueurRandom
from JoueurTetu import JoueurTetu
from JoueurMeilleureReponse import JoueurMeilleureReponse
from JoueurStochastique import JoueurStochastique
from JoueurFictitiousPlay import JoueurFictitiousPlay


joueur_0 = None
joueur_1 = None
"""
    MODE :
        0: normale
        1: budget fixe pour chaque militant
        2: budget compagne entière
"""
m_0 = 2
m_1 = 2


joueur_0 = JoueurMeilleureReponse(m_0)
joueur_1 = JoueurTetu(m_1)

# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----




# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'blottoMap'
    game = Game('./Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 100 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)


    nb_partie_count = 0
    nb_partie = 5
    while nb_partie_count < nb_partie:
        init()



        #-------------------------------
        # Initialisation
        #-------------------------------

        nbLignes = game.spriteBuilder.rowsize
        nbCols = game.spriteBuilder.colsize

        print("lignes", nbLignes)
        print("colonnes", nbCols)


        players = [o for o in game.layers['joueur']]
        nbPlayers = len(players)
        print("Trouvé ", nbPlayers, " militants")



        # on localise tous les états initiaux (loc du joueur)
        # positions initiales des joueurs
        initStates = [o.get_rowcol() for o in players]
        print ("Init states:", initStates)

        joueur_0.updateInitStateSrpite([initStates[i] for i in range(len(initStates)) if i%2==0]) #get initstate pour calculer cout (mode 1, mode 2)
        joueur_1.updateInitStateSrpite([initStates[i] for i in range(len(initStates)) if i%2==1]) #get initstate pour calculer cout (mode 1, mode 2)

        # on localise tous les secteurs d'interet (les votants)
        # sur le layer ramassable
        goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
        print ("Goal states:", goalStates)



        # on localise tous les murs
        # sur le layer obstacle
        wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
        print ("Wall states:", wallStates)

        def legal_position(row,col):
            # une position legale est dans la carte et pas sur un mur
            return ((row,col) not in wallStates) and row>=0 and row<nbLignes and col>=0 and col<nbCols

        def goalRandom(init, nb_electeur=5):
            goal = []
            for i in range(nb_electeur):
                r, c = (random.randint(0, nbLignes-1), random.randint(0, nbCols-1)) #random pos sur la grille
                while not legal_position(r, c) or (r, c) in init or (r, c) in goal: # pos légale
                    r, c = (random.randint(0, nbLignes - 1), random.randint(0, nbCols - 1))
                goal.append((r, c))
            return goal

        #allouer random electeurs
        #goalStates = goalRandom(initStates)



        #-------------------------------
        # Attributaion aleatoire des fioles
        #-------------------------------

        objectifs = goalStates
        # random.shuffle(objectifs)
        #Pour compter des points
        liste_j0 = joueur_0.choisirElecteurs(objectifs, nbPlayers//2)
        liste_j1 = joueur_1.choisirElecteurs(objectifs, nbPlayers//2)

        #Pour se deplacer
        j0_init = joueur_0.getInitStateSrpite()
        j1_init = joueur_1.getInitStateSrpite()

        liste_j0_deplace = copy.deepcopy(liste_j0)
        liste_j1_deplace = copy.deepcopy(liste_j1)
        print(liste_j1)
        for i in range(len(liste_j0_deplace)): #les militants qui n'atteintent aucune cible vont rester à leur pos initiale
            if liste_j0[i] == (-1, -1):
                liste_j0_deplace[i] = j0_init[i]
            if liste_j1[i] == (-1, -1):
                liste_j1_deplace[i] = j1_init[i]

        liste_choix = []
        for i in range(len(liste_j0_deplace)):
            liste_choix.append(liste_j0_deplace[i])
            liste_choix.append(liste_j1_deplace[i])
        #liste_choix = liste_j0_deplace + liste_j1_deplace
        print(liste_choix)
        # for i in range(nbPlayers): #Chaque militant choisit une cible random
        #     liste_choix.append(random.choice(objectifs))
        # # print("Objectif joueur 0", objectifs[0])
        # # print("Objectif joueur 1", objectifs[1])
        # liste_j0 = liste_choix[:len(liste_choix)//2]
        # liste_j1 = liste_choix[len(liste_choix) // 2:]




        #-------------------------------
        # Carte demo
        # 2 joueurs
        # Joueur 0: A*
        # Joueur 1: random walk
        #-------------------------------

        #-------------------------------
        # calcul A* pour le joueur 0
        #-------------------------------



        g =np.ones((nbLignes,nbCols),dtype=bool)  # par defaut la matrice comprend des True
        for w in wallStates:            # putting False for walls
            g[w]=False
        liste_path = []
        for i in range(nbPlayers):
            liste_path.append(probleme.astar(ProblemeGrid2D(initStates[i],liste_choix[i],g,'manhattan')))
        # p = ProblemeGrid2D(initStates[0],objectifs[0],g,'manhattan')
        # path = probleme.astar(p)
        print ("Chemin trouvé:", liste_path)


        #-------------------------------
        # Boucle principale de déplacements
        #-------------------------------


        posPlayers = initStates
        list_sprite = [i for i in range(nbPlayers)]
        fini = []
        print("PATH", liste_path)
        for i in range(iterations):
            if len(fini) == nbPlayers:
                break
            # on fait bouger chaque joueur séquentiellement


            # Joeur 0: suit son chemin trouve avec A*

            for j in list_sprite:
                if j not in fini:
                    # print("J", j, "iter", i)
                    # print("CHOIX", liste_choix[j])
                    # print("FINI", fini)
                    # print(liste_path[j])
                    row, col = liste_path[j][i]
                    posPlayers[j] = (row, col)
                    players[j].set_rowcol(row, col)
                    #print("pos {}:".format(j), row, col)
                    if (row, col) == liste_choix[j]:
                        #print("le joueur {} a atteint son but!".format(j))
                        fini.append(j)


            # row,col = path[i]
            # posPlayers[0]=(row,col)
            # players[0].set_rowcol(row,col)
            # print ("pos 0:", row,col)
            # if (row,col) == objectifs[0]:
            #     print("le joueur 0 a atteint son but!")
            #     break
            #
            # # Joueur 1: fait du random walk
            #
            # # row,col = posPlayers[1]
            # #
            # # while True: # tant que pas legal on retire une position
            # #     x_inc,y_inc = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
            # #     next_row = row+x_inc
            # #     next_col = col+y_inc
            # #     if legal_position(next_row,next_col):
            # #         break
            # # players[1].set_rowcol(next_row,next_col)
            # # print ("pos 1:", next_row,next_col)
            # #
            # # col=next_col
            # # row=next_row
            # # posPlayers[1]=(row,col)
            # row, col = path[i]
            # posPlayers[1] = (row, col)
            # players[1].set_rowcol(row, col)
            # print("pos 0:", row, col)
            # if (row, col) == objectifs[0]:
            #     print("le joueur 0 a atteint son but!")
            #     break
            # if (row,col) == objectifs[1]:
            #     print("le joueur 1 a atteint son but!")
            #     break



            # on passe a l'iteration suivante du jeu
            game.mainiteration()


        print(liste_j0)
        print(liste_j1)

        liste_choix_score = [x for x in liste_choix if x != (-1, -1)]
        liste_j0_score = [x for x in liste_j0 if x != (-1, -1)]
        liste_j1_score = [x for x in liste_j1 if x != (-1, -1)]

        choix_nom = list(set(liste_choix_score))
        dic_0 = {}
        dic_1 = {}
        for ele in choix_nom:
            dic_0[ele] = 0
            dic_1[ele] = 0
        for i in range(len(liste_j0_score)):
            dic_0[liste_j0_score[i]] += 1
        for i in range(len(liste_j1_score)):
            dic_1[liste_j1_score[i]] += 1
        cpt0 = 0
        cpt1 = 0
        for ele in choix_nom:
            if dic_0[ele] > dic_1[ele]:
                cpt0 += 1
            elif dic_0[ele] < dic_1[ele]:
                cpt1 += 1
        print(cpt0, cpt1)
        if cpt0 > cpt1:
            res_0 = 1
            res_1 = -1
            print("Joueur 0 gagne !!")
        elif cpt0 < cpt1:
            res_0 = -1
            res_1 = 1
            print("Joueur 1 gagne !!")
        else:
            res_0 = 0
            res_1 = 0
            print("Partie nulle")
        time.sleep(5)
        nb_partie_count += 1

        joueur_0.sauvergarder(liste_j0, liste_j1, res_0, joueur_1.stratChoisie())
        joueur_1.sauvergarder(liste_j1, liste_j0, res_1, joueur_0.stratChoisie())

    pygame.quit()
    
    
    
    
    #-------------------------------
    
        
        
    
    
        
    
   

if __name__ == '__main__':
    main()
    


