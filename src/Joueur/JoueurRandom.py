import random
from Joueur import Joueur

def creerJoueur(m=0, budget=None):
    return JoueurRandom(m, budget)

def distManhattan(p1,p2):
    """ calcule la distance de Manhattan entre le tuple
        p1 et le tuple p2
        """
    (x1,y1)=p1
    (x2,y2)=p2
    return abs(x1-x2)+abs(y1-y2)

class JoueurRandom(Joueur):
    def choisirElecteurs(self, obj, nbMilitants):
        if self.mode == 0:
            liste_choix = []
            for i in range(nbMilitants):  # Chaque militant choisit une cible random
                liste_choix.append(random.choice(obj))
            return liste_choix
        elif self.mode == 1:
            liste_choix = []
            for i in range(nbMilitants):
                militant = self.initState[i] #recupperer les militants 1 par 1 pour calculer la distance
                listePossibilite = list(filter(lambda x: distManhattan(militant, x) <= self.cout_militant_mode_1, obj)) #liste destination possible
                if listePossibilite != []:
                    liste_choix.append(random.choice(listePossibilite))
                else:
                    liste_choix.append((-1, -1)) #pour indiquer que ce militant ne trouve pas une cible possible
            return liste_choix

        elif self.mode == 2:
            liste_choix = []
            for i in range(nbMilitants):  # Chaque militant choisit une cible random
                militant = self.initState[i]  # recupperer les militants 1 par 1 pour calculer la distance
                listePossibilite = list(filter(lambda x: distManhattan(militant, x) <= self.budget, obj))  # liste destination possible dont cout <= budget
                if listePossibilite != []:
                    choix_fait = random.choice(listePossibilite)
                    dist = distManhattan(militant, choix_fait)
                    self.budget -= dist # Mettre à jour le budget
                    liste_choix.append(choix_fait)
                else:
                    liste_choix.append((-1, -1)) #pour indiquer que ce militant ne trouve pas une cible possible
            return liste_choix




    def stratChoisie(self):
        return 0