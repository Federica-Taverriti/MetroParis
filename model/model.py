from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate() #riempito di oggetti "Fermata"
        self._grafo = nx.DiGraph() #istanziato il grafo orientato
        self._idMapFermate = {}
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f #dato id_fermato ritorno il tipo Fermata corrispondente

    def buildGraph(self):
        self._grafo.clear() #svuoto grafo iniziale prima di farne un'altro
        self._grafo.add_nodes_from(self._fermate) #popolare grafo con lista di fermate
        self.addedges3()

   # due cicli for impiega molto tempo per vedere tutte le coppie
    def addedges(self):
        for u in self._fermate:
            for v in self._fermate:
                if DAO.hasconn(u,v): #se true aggiungi
                    self._grafo.add_edge(u,v)

    #strategia migliore che impiega meno tempo; ciclo su tutte le fermate e per ognuna prendo i vicini connessi
    def addedges2(self):
        for u in self._fermate:
            for conn in DAO.getvicini(u):
                v = self._idMapFermate[conn.id_stazA]
                self._grafo.add_edge(u,v)

    def addedges3(self):
        alledges = DAO.getAllEdges()
        for conn in alledges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]
            self._grafo.add_edge(u,v)



    def get_numnodi(self):
        return len(self._grafo.nodes())

    def get_numarchi(self):
        return len(self._grafo.edges())

    @property
    def fermate(self):
        return self._fermate