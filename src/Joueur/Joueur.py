class Joueur:
    def __init__(self, mode=0, budget=None):
        """
        :param mode: 0 - mode normal, il n'y a pas de contraintes
                     1 - le budget est fixe pour chaque militant
                     2 - budget total
        """
        self.mode = mode
        if self.mode == 1: #distance que chaque militant peut se déplacer pendant une journée
            self.cout_militant_mode_1 = 18
        elif self.mode == 2: #distance TOTALE pour une campagne
            if budget is None:
                self.budget = 250
            else:
                self.budget = budget

    def choisirElecteurs(self, obj, nbMilitants):
        raise NotImplementedError("Faites le")

    def stratChoisie(self):
        raise NotImplementedError("Faites le")

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

    def getInitStateSrpite(self):
        return self.initState