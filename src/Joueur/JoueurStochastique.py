import JoueurRandom
import JoueurTetu
import JoueurMeilleureReponse
import JoueurFictitiousPlay
from Joueur import Joueur


import random
liste_strate = [JoueurRandom, JoueurTetu, JoueurMeilleureReponse, JoueurFictitiousPlay]
liste_distri = [0.1, 0.0, 0.9, 0.0]

def creerJoueur(m=0, budget=None):
    return JoueurStochastique(m, budget)

def distManhattan(p1,p2):
    """ calcule la distance de Manhattan entre le tuple
        p1 et le tuple p2
        """
    (x1,y1)=p1
    (x2,y2)=p2
    return abs(x1-x2)+abs(y1-y2)

class JoueurStochastique(Joueur):
    def __init__(self, mode=0, budget=None):
        super().__init__(mode, budget)
        self.strate_adv_prec = None


    def choisirElecteurs(self, obj, nbMilitants):
        choix_strate = random.choices(liste_strate, liste_distri)[0]
        print(choix_strate)
        if self.mode == 2:
            jx = choix_strate.creerJoueur(self.mode, self.budget)
        else:
            jx = choix_strate.creerJoueur(self.mode)
        jx.updateInitStateSrpite(self.initState)
        if self.strate_adv_prec is not None:
            jx.sauvergarder(self.ma_strate, self.sa_strate, self.res_prec, self.strate_adv_prec)
        choix = jx.choisirElecteurs(obj, nbMilitants)
        if self.mode == 2:
            self.budget = jx.budget
        return choix

    def stratChoisie(self):
        return 3

    def sauvergarder(self, choix1, choix2, res, strat_adv):
        """
        sauvergarder la strat jouée
        :param choix1: ma strategie
        :param choix2: sa strategie
        :param res: 1 gagné, -1 perdu, 0 null
        :param strat_adv: strategie utilisée par adv
        :return:
        """
        self.ma_strate = choix1
        self.sa_strate = choix2
        self.res_prec = res
        self.strate_adv_prec = strat_adv

    def updateInitStateSrpite(self, liste_init):
        self.initState = liste_init


