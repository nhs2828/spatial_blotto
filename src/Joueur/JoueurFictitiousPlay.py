import random
from Joueur import Joueur
import JoueurRandom
import JoueurTetu
import JoueurMeilleureReponse
import JoueurStochastique

def creerJoueur(m=0, budget=None):
    return JoueurFictitiousPlay(m, budget)

def distManhattan(p1,p2):
    """ calcule la distance de Manhattan entre le tuple
        p1 et le tuple p2
        """
    (x1,y1)=p1
    (x2,y2)=p2
    return abs(x1-x2)+abs(y1-y2)

class JoueurFictitiousPlay(Joueur):
    def __init__(self, mode=0, budget=None):
        super().__init__(mode, budget)
        self.res_prec = -2  # debut
        self.tab_strategie = [JoueurRandom, JoueurTetu, JoueurMeilleureReponse, JoueurStochastique]  # ordre fixé pour construire matrice
        """
            Version 1: Nous initialisons la matrice random
        """
        self.matrice = [[(random.randint(1,3), (random.randint(1,3))) for i in range(len(self.tab_strategie))] for j in range(len(self.tab_strategie))]
        """
            Version 2: Comme dans le TD, R et B ont tendance de joueur la même strategie
        """
        # for i in range(len(self.tab_strategie)):
        #     for j in range(len(self.tab_strategie)):
        #         if i==j:
        #             self.matrice[i][j] = (3, 3)
        #         else:
        #             self.matrice[i][j] = (0, 0)

        # Pour etre simple, je pré-définie les situations, pour joueur c'est les lignes, adv est les colonnes (joueur R, adv B comme dans TD)
        # les 2 joueurs ont tendance de jouer meme strategie
        self.dic = {} #pour observer les strategies jouées
        self.strate_adv_prec = None #debut
        for i in range(len(self.tab_strategie)):
            self.dic[i] = 1 #je donne 1 pour ne pas sur-favoriser une strategie qui mene à la convergence

    def choisirElecteurs(self, obj, nbMilitants):
        #Preparation
        if self.strate_adv_prec is not None:
            self.dic[self.strate_adv_prec] += 1 # mettre à jour le dictionnaire

        proba_best = -1
        action = -1
        somme = 0
        for i in range(len(self.tab_strategie)):
            somme += self.dic[i]

        for i in range(len(self.tab_strategie)):
            proba_total = 0
            for j in range(len(self.tab_strategie)):
                proba = self.dic[j]/somme
                proba_total += self.matrice[j][i][0]*proba #matrice[x][y] -> (a, b) -> a est le notre, b est de notre adv
            if proba_total > proba_best:
                proba_best = proba_total
                action = i

        self.strategie = self.tab_strategie[action]
        print("STRATE ICI", self.strategie)
        if self.mode != 2:
            j = self.strategie.creerJoueur(self.mode)
        else:
            j = self.strategie.creerJoueur(self.mode, self.budget)
        """
            Nous donnons à joueur fictif crée nos statisques
        """
        j.updateInitStateSrpite(self.initState)
        if self.strate_adv_prec is not None:
            j.sauvergarder(self.ma_strate, self.sa_strate, self.res_prec, self.strate_adv_prec)
        choix = j.choisirElecteurs(obj, nbMilitants)
        if self.mode == 2:
            self.budget = j.budget
        return choix

    def stratChoisie(self):
        return self.tab_strategie.index(self.strategie)

