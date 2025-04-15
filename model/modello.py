import copy
import datetime
from types import NoneType

from database.DAO import DAO
from model.nerc import Nerc


class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()
        self.affetti_Tot=0
        self._totOre=0

    def worstCase(self, nerc, maxY, maxH):
        """ritorna la sequenza ottima che massimizza il numero di effetti e il valore della funz obiettivo
           nel caso in cui esistano eventi per il nerc specificato, restituisce una lista vuota altrimenti"""
        self._solBest=[]
        self.loadEvents(nerc)
        self.affetti_Tot=0
        self._totOre = 0
        if len(self._listEvents)==0:
            return None
        else:
            self._ricorsione([],maxY, maxH, self._listEvents)
            return self._solBest, self.affetti_Tot, self._totOre

    def pazienti_affetti(self, parziale):
        """calcola il numero totale di persone coinvolte in base alla sequenza indicata"""
        tot_affetti=0
        for evento in parziale:
            tot_affetti+=evento.customers_affected
        return tot_affetti

    def calcola_ore(self, parziale):
        """calcola il numero totale di ore di blackout in base alla sequenza indicata"""
        ore_parziale=0
        for evento in parziale:
            ore_parziale += evento.ore_disservizio()
        return ore_parziale

    def calcola_anno(self, parziale):
        """restituisce l'anno minimo e l'anno massimo della sequenza indicata"""
        anno_max=0
        anno_min=100000

        for evento in parziale:
            if evento.date_event_began.year>anno_max:
                anno_max=evento.date_event_began.year
            if evento.date_event_finished.year<anno_min:
                anno_min=evento.date_event_finished.year
        return anno_max,anno_min

    def is_admisible(self, parziale, maxY, maxH, evento):
        """restituisce true se la soluzione (parziale+evento) rispetta i vincoli, altrimenti
           restituisce false"""
        ore=self.calcola_ore(parziale)
        amax, amin=self.calcola_anno(parziale)
        if ore+evento.ore_disservizio()<=maxH and (max(amax, evento.date_event_began.year)-min(amin,evento.date_event_began.year))<=maxY:
            return True
        else:
            return False

    def _ricorsione(self, parziale, maxY, maxH, pos):
        """algoritmo ricorsivo che esplora tutte le soluzioni ammissibili"""
        if self.pazienti_affetti(parziale) > self.affetti_Tot:
            self._solBest = copy.deepcopy(parziale)
            self.affetti_Tot = self.pazienti_affetti(parziale)
            self._totOre = self.calcola_ore(parziale)

        for i in range(0,len(pos)):
            if self.is_admisible(parziale, maxY, maxH, pos[i]):
                parziale.append(pos[i])
                self._ricorsione(parziale, maxY, maxH, pos[i+1:])
                parziale.pop()

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()

    @property
    def listNerc(self):
        return self._listNerc

if __name__ == '__main__':
    my_model=Model()
    my_model.worstCase(Nerc(1,"ERCOT"), 4, 200)
    print(my_model.affetti_Tot)
    print(my_model._solBest)
    print(my_model._totOre)
