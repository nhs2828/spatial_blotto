import random
from Joueur import Joueur

def creerJoueur(m=0, budget=None):
    return JoueurTetu(m, budget)

def distManhattan(p1,p2):
    """ calcule la distance de Manhattan entre le tuple
        p1 et le tuple p2
        """
    (x1,y1)=p1
    (x2,y2)=p2
    return abs(x1-x2)+abs(y1-y2)

class JoueurTetu(Joueur):
    def __init__(self, mode=0, budget=None, choix=None):
        super().__init__(mode, budget)
        self.strategieTT = choix #Nous fixons la strategie pour ce joueur !

    def choisirElecteurs(self, obj, nbMilitants):
        if self.strategieTT is None:
            if self.mode == 0:
                liste_choix = []
                for i in range(nbMilitants):  # Chaque militant choisit une cible random
                    liste_choix.append(random.choice(obj))

                self.strategieTT = liste_choix #Engregister
                return liste_choix
            elif self.mode == 1:
                liste_choix = []
                for i in range(nbMilitants):
                    militant = self.initState[i]  # recupperer les militants 1 par 1 pour calculer la distance
                    listePossibilite = list(filter(lambda x: distManhattan(militant, x) <= self.cout_militant_mode_1,
                                                   obj))  # liste destination possible
                    if listePossibilite != []:
                        liste_choix.append(random.choice(listePossibilite))
                    else:
                        liste_choix.append((-1, -1))  # pour indiquer que ce militant ne trouve pas une cible possible
                self.strategieTT = liste_choix  # Engregister
                return liste_choix

            elif self.mode == 2:
                liste_choix = []
                for i in range(nbMilitants):  # Chaque militant choisit une cible random
                    militant = self.initState[i]  # recupperer les militants 1 par 1 pour calculer la distance
                    listePossibilite = list(filter(lambda x: distManhattan(militant, x) <= self.budget,
                                                   obj))  # liste destination possible dont cout <= budget
                    if listePossibilite != []:
                        choix_fait = random.choice(listePossibilite)
                        dist = distManhattan(militant, choix_fait)
                        self.budget -= dist  # Mettre à jour le budget
                        liste_choix.append(choix_fait)
                    else:
                        liste_choix.append((-1, -1))  # pour indiquer que ce militant ne trouve pas une cible possible

                self.strategieTT = liste_choix  # Engregister
                return liste_choix
        else:
            if self.mode == 0 or self.mode == 1:
                return self.strategieTT
            else: #mode budget
                liste_choix = []
                for i in range(len(self.strategieTT)):
                    dist = distManhattan(self.initState[i], self.strategieTT[i])
                    if dist <= self.budget:
                        liste_choix.append(self.strategieTT[i])
                        self.budget -= dist
                    else:
                        liste_choix.append((-1, -1))
                return liste_choix


    def stratChoisie(self):
        return 1