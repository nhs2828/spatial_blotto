import random
import numpy as np
import copy as cp
from Joueur import Joueur

def creerJoueur(m=0, budget=None):
    return JoueurMeilleureReponse(m, budget)

def distManhattan(p1,p2):
    """ calcule la distance de Manhattan entre le tuple
        p1 et le tuple p2
        """
    (x1,y1)=p1
    (x2,y2)=p2
    return abs(x1-x2)+abs(y1-y2)

def liste_couple_vers_liste_choix(liste_couple, init_state):
    """
    Liste couple militants-son choix -> liste des choix dont indice sont les indice des militants dans liste ini_state
    :param liste_couple: liste des couples militant-le_choix_fait.
        Exp ((1,1), (3,4)):
            -> (1,1) coordonnées du militant
            -> (3,4) coordonnées de l'electeur choisi
    :param init_state: liste des coordonnées initiales des militants
    :return: liste des choix faits par militants
    """
    liste_choix = []  # liste couple-destination -> liste destination
    for i in range(len(init_state)):
        ok = False
        for j in liste_couple:
            mili, des = j
            if init_state[i] == mili:
                liste_choix.append(des)
                ok = True
                break
        if not ok:  # si ce mililant n'atteint aucune cible -> il bougera pas -> (-1, -1)
            liste_choix.append((-1, -1))
    return liste_choix

def peutGagner(ma_strate, sa_strate, objectifs):
    """
    :param ma_strate: les choix des nos militants
    :param sa_strate: les choix des militants adversaires
    :param objectifs: les coordonnées des objectifs
    :return: si ma strategie peut vaincre la strategie adversaire : True
            sinon : False
    """
    mon_score = [x for x in ma_strate if x != (-1, -1)]
    son_score = [x for x in sa_strate if x != (-1, -1)]

    dic_0 = {}
    dic_1 = {}
    for ele in objectifs:
        dic_0[ele] = 0
        dic_1[ele] = 0
    for i in range(len(mon_score)):
        dic_0[mon_score[i]] += 1
    for i in range(len(son_score)):
        dic_1[son_score[i]] += 1
    cpt0 = 0
    cpt1 = 0
    for ele in objectifs:
        if dic_0[ele] > dic_1[ele]:
            cpt0 += 1
        elif dic_0[ele] < dic_1[ele]:
            cpt1 += 1
    if cpt0 > cpt1:
        return True
    return False

class JoueurMeilleureReponse(Joueur):
    def __init__(self, mode, budget=None):
        super().__init__(mode, budget)
        self.res_prec = None #debut


    def choisirElecteurs(self, obj, nbMilitants):
        print("INIT", self.initState)
        if self.mode == 0:
            if self.res_prec is None: #debut -> je joue random
                liste_choix = []
                for i in range(nbMilitants):  # Chaque militant choisit une cible random
                    liste_choix.append(random.choice(obj))
                return liste_choix
            elif self.res_prec == 1: #si j'ai gagné dans la partie précedente -> je joue comme avant
                return self.ma_strate
            else: #Sinon je trouve une autre strategie qui bat la strategie précedente de l'adversaire
                des_adv = [i for i in self.sa_strate if i != (-1, -1)]
                nb_militant_destination = [0 for i in range(len(obj))]
                for i in des_adv:
                    ind = obj.index(i)
                    nb_militant_destination[ind] += 1
                ordre_ajouter = np.argsort(nb_militant_destination)
                pos_init = cp.deepcopy(self.initState)
                liste_couple_mili_des = []

                for inx in ordre_ajouter:  # parcourir les endroits ayant le moins nombres de militants adversaires
                    if pos_init == []: #s'il n'y a plus de militants dispo => nous arretons
                        break
                    for y in range(nb_militant_destination[inx] + 1):  # nous mettons à cet endroit nbMilitant d'adv + 1 pour gagner cet endroit
                        if pos_init == []: #s'il n'y a plus de militants dispo => nous arretons
                            break
                        militant_choisi = pos_init[0]
                        liste_couple_mili_des.append([militant_choisi, obj[inx]])  # ajoute le couple militant-destination
                        pos_init.remove(militant_choisi)  # enlever le militant choisi

                """
                    Liste couple militant-destination en liste de choix
                """
                liste_choix = liste_couple_vers_liste_choix(liste_couple_mili_des, self.initState)  # liste couple-destination -> liste destination
                return liste_choix
        elif self.mode == 1:
            if self.res_prec is None: #debut -> je joue random
                liste_choix = []
                for i in range(nbMilitants):
                    militant = self.initState[i]  # recupperer les militants 1 par 1 pour calculer la distance
                    listePossibilite = list(filter(lambda x: distManhattan(militant, x) <= self.cout_militant_mode_1,
                                                   obj))  # liste destination possible
                    if listePossibilite != []:
                        liste_choix.append(random.choice(listePossibilite))
                    else:
                        liste_choix.append((-1, -1))  # pour indiquer que ce militant ne trouve pas une cible possible
                return liste_choix
            elif self.res_prec == 1: #si j'ai gagné dans la partie précedente -> je joue comme avant
                return self.ma_strate
            else: #Sinon je trouve une autre strategie qui bat la strategie précedente de l'adversaire
                des_adv = [i for i in self.sa_strate if i != (-1, -1)]
                nb_militant_destination = [0 for i in range(len(obj))]
                for i in des_adv:
                    ind = obj.index(i)
                    nb_militant_destination[ind] += 1
                ordre_ajouter = np.argsort(nb_militant_destination)
                pos_init = cp.deepcopy(self.initState)
                liste_couple_mili_des = []
                liste_des_non_reussi = []

                for inx in ordre_ajouter: # parcourir les endroits ayant le moins nombres de militants adversaires
                    liste_pos_init_origine = cp.deepcopy(pos_init)
                    liste_couple_mili_des_origine = cp.deepcopy(liste_couple_mili_des)
                    reussi = 0 #pour compter le nombre de militant déployé
                    for y in range(nb_militant_destination[inx] + 1): #nous mettons à cet endroit nbMilitant d'adv + 1 pour gagner cet endroit
                        dis_min = 999999
                        militant_choisi = -1
                        for i in range(len(pos_init)): #parcourir nos militants pour trouver celui qui est le plus proche
                            dist = distManhattan(pos_init[i], obj[inx])
                            if dist < dis_min and dist <= self.cout_militant_mode_1: #si plus proche ET avoir assez de budget
                                dis_min = dist
                                militant_choisi = i
                        if militant_choisi != -1: #si nous arrivons à trouver un candidat
                            reussi += 1
                            liste_couple_mili_des.append([pos_init[militant_choisi], obj[inx]]) #ajoute le couple militant-destination
                            pos_init.remove(pos_init[militant_choisi]) #enlever le militant choisi
                    """
                        si nous avons pas assez de militants pour cet electeur, nous passons à electeur suivant pour
                        ne pas gaspiller les militants
                    """
                    if reussi != nb_militant_destination[inx]+1:
                        liste_des_non_reussi.append(cp.deepcopy(inx))
                        liste_couple_mili_des = cp.deepcopy(liste_couple_mili_des_origine) #reset liste couple
                        pos_init = cp.deepcopy(liste_pos_init_origine) #reset pos_init

                """
                    Après la boucle s'il reste encore des éléments dans pos_ini
                    => ce sont des militants qui ne peuvent pas trouver une cible pour avoir une meilleure réponse
                    => Nous les déployons aux destinations non réussi si possible es espérant d'voir un score nul pour
                    cette destination
                """

                for inx in liste_des_non_reussi:
                    for y in range(nb_militant_destination[inx]):  # nous mettons à cet endroit nbMilitant d'adv pour avoir un resultat nul
                        dis_min = 999999
                        militant_choisi = -1
                        for i in range(len(pos_init)):  # parcourir nos militants pour trouver celui qui est le plus proche
                            dist = distManhattan(pos_init[i], obj[inx])
                            if dist < dis_min and dist <= self.cout_militant_mode_1:  # si plus proche ET avoir assez de budget
                                dis_min = dist
                                militant_choisi = i
                        if militant_choisi != -1:  # si nous arrivons à trouver un candidat
                            liste_couple_mili_des.append([pos_init[militant_choisi], obj[inx]])  # ajoute le couple militant-destination
                            pos_init.remove(pos_init[militant_choisi])  # enlever le militant choisi
                """
                    Liste couple militant-destination en liste de choix
                """
                liste_choix = liste_couple_vers_liste_choix(liste_couple_mili_des, self.initState) #liste couple-destination -> liste destination
                # for i in range(len(self.initState)):
                #     ok = False
                #     for j in liste_couple_mili_des:
                #         mili, des = j
                #         if self.initState[i] == mili:
                #             liste_choix.append(des)
                #             ok = True
                #             break
                #     if not ok: #si ce mililant n'atteint aucune cible -> il bougera pas -> (-1, -1)
                #         liste_choix.append((-1, -1))
                return liste_choix
        elif self.mode == 2:
            if self.res_prec is None:  # debut -> je joue random
                liste_choix = []
                for i in range(nbMilitants):
                    militant = self.initState[i]  # recupperer les militants 1 par 1 pour calculer la distance
                    listePossibilite = list(filter(lambda x: distManhattan(militant, x) <= self.budget, obj))  # liste destination possible
                    """
                        Nous choisissons random pour ne pas favoriser des distances courtes
                    """
                    if listePossibilite != []:
                        choix = random.choice(listePossibilite)
                        liste_choix.append(choix)
                        self.budget -= distManhattan(militant, choix) #Nous diminuons le budget un cout de distance
                    else:
                        liste_choix.append((-1, -1))  # pour indiquer que ce militant ne trouve pas une cible possible
                return liste_choix
            else: #Re-calculer les choix a cause du risque d'avoir pas assez de budget
                des_adv = [i for i in self.sa_strate if i != (-1, -1)]
                nb_militant_destination = [0 for i in range(len(obj))]
                for i in des_adv:
                    ind = obj.index(i)
                    nb_militant_destination[ind] += 1
                ordre_ajouter = np.argsort(nb_militant_destination)
                pos_init = cp.deepcopy(self.initState)
                liste_couple_mili_des = []
                liste_des_non_reussi = []

                for inx in ordre_ajouter:  # parcourir les endroits ayant le moins nombres de militants adversaires
                    test_gagner = liste_couple_vers_liste_choix(liste_couple_mili_des, self.initState)
                    if peutGagner(test_gagner, self.sa_strate, obj):
                        break
                    liste_pos_init_origine = cp.deepcopy(pos_init)
                    liste_couple_mili_des_origine = cp.deepcopy(liste_couple_mili_des)
                    budget_origine = cp.deepcopy(self.budget)
                    reussi = 0  # pour compter le nombre de militant déployé
                    for y in range(nb_militant_destination[inx] + 1):  # nous mettons à cet endroit nbMilitant d'adv + 1 pour gagner cet endroit
                        dis_min = 999999
                        militant_choisi = -1
                        for i in range(len(pos_init)):  # parcourir nos militants pour trouver celui qui est le plus proche
                            dist = distManhattan(pos_init[i], obj[inx])
                            if dist < dis_min and dist <= self.budget:  # si plus proche ET avoir assez de budget
                                dis_min = dist
                                militant_choisi = i
                        if militant_choisi != -1:  # si nous arrivons à trouver un candidat
                            reussi += 1
                            self.budget -= distManhattan(pos_init[militant_choisi], obj[inx]) #Diminuer le budget
                            liste_couple_mili_des.append([pos_init[militant_choisi], obj[inx]])  # ajoute le couple militant-destination
                            pos_init.remove(pos_init[militant_choisi])  # enlever le militant choisi
                    """
                        si nous avons pas assez de militants pour cet electeur (a cause du budget insuffisant, nous passons à electeur suivant pour
                        ne pas gaspiller les militants et le budget
                    """
                    if reussi != nb_militant_destination[inx] + 1:
                        self.budget = cp.deepcopy(budget_origine) #Restaurer le budget
                        liste_des_non_reussi.append(cp.deepcopy(inx))
                        liste_couple_mili_des = cp.deepcopy(liste_couple_mili_des_origine)  # reset liste couple
                        pos_init = cp.deepcopy(liste_pos_init_origine)  # reset pos_init

                """
                    Après la boucle s'il reste encore des éléments dans pos_ini
                    => ce sont des militants qui ne peuvent pas trouver une cible pour avoir une meilleure réponse
                    => Nous ne faisons rien avec eux pour économiser le budget
                """


                """
                    Liste couple militant-destination en liste de choix
                """
                liste_choix = liste_couple_vers_liste_choix(liste_couple_mili_des, self.initState)
                return liste_choix


    def stratChoisie(self):
        return 2

