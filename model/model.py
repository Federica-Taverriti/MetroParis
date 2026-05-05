from database.DAO import DAO
import networkx as nx
from datetime import datetime

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate() #riempito di oggetti "Fermata"
        self._grafo = nx.DiGraph() #istanziato il grafo orientato; anche per grafo pesato
        #self._grafo = nx.MultiDiGraph()
        self._idMapFermate = {}
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f #dato id_fermato ritorno il tipo Fermata corrispondente

    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgesPesati()

    def addEdgesPesati(self):
        #riutilizzare il principio di funzionamento del metodo addedges3
        #ma contando quante volte provo ad aggiungere l'arco
        self._grafo.clear_edges()
        alledges = DAO.getAllEdges()
        for conn in alledges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]

            if self._grafo.has_edge(u,v): #se c'è un acro tra u e v implemento peso
                self._grafo[u][v]["weight"] += 1 #accedo al grafo sfruttando il fatto che è definito come un dizionario
            else: #se non c'è arco, lo creo dandogli peso 1
                self._grafo.add_edge(u,v, weight = 1)

    def addEdgesPesatiV2(self):
        #delega il calcolo del peso alla query sql, per semplificare python
        self._grafo.clear_edges()
        allEdgesWPeso = DAO.getAllEdgesPesati()
        # (id_stazP, id_stazA, peso) tupla che ricevo

        for e in allEdgesWPeso:
            u = self._idMapFermate[e[0]]
            v = self._idMapFermate[e[1]]
            peso = e[2]
            self._grafo.add_edge(u, v, weight = peso)

    def getArchiPesoMaggiore(self):
        edges = self._grafo.edges(data = True) #salvo archi con tutti gli attributi (default sarebbe data=False, che non salva attributi e quindi senza salvare peso)

        edgesMaggiori = []
        for e in edges:
            if self._grafo.get_edge_data(e[0], e[1])["weight"] > 1:
                #self._grafo[e[0]][e[1]]["weight"] accedere in modo posizionale?
                edgesMaggiori.append(e)
        return edgesMaggiori

    # 4 esplorazioni: 2 BFS e 2 DFS
    def getBFSNodesFromEdges(self, source): #da nodo "source"
        archi = nx.bfs_edges(self._grafo, source) #iterable di tuple, quindi si possono ciclare
        nodiBFS = []
        for u, v in archi:
            nodiBFS.append(v) #aggiungiamo nodo di arrivo
        return nodiBFS

    def getBFSNodesFromTree(self, source):
        tree = nx.bfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi #contiene anche source

    def getDFSNodesFromEdges(self, source): #da nodo "source"
        archi = nx.dfs_edges(self._grafo, source)
        nodiDFS = []
        for u, v in archi:
            nodiDFS.append(v) #aggiungiamo nodo di arrivo
        return nodiDFS

    def getDFSNodesFromTree(self, source):
        tree = nx.dfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi #contiene anche source


    def buildGraph(self):
        self._grafo.clear() #svuoto grafo iniziale prima di farne un'altro
        self._grafo.add_nodes_from(self._fermate) #popolare grafo con lista di fermate

        # tic = datetime.now()
        # self.addedges()
        # toc = datetime.now()
        # print("Tempo impiegato da modo 1: ", toc-tic)

        # tic = datetime.now()
        # self.addedges2()
        # toc = datetime.now()
        # print("Tempo impiegato da modo 2: ", toc - tic)

        tic = datetime.now()
        self.addedges3()
        toc = datetime.now()
        print("Tempo impiegato da modo 3: ", toc - tic)

   # due cicli for impiega molto tempo per vedere tutte le coppie
    def addedges(self):
        self._grafo.clear_edges()
        for u in self._fermate:
            for v in self._fermate:
                if DAO.hasconn(u,v): #se true aggiungi
                    self._grafo.add_edge(u,v)

    #strategia migliore che impiega meno tempo; ciclo su tutte le fermate e per ognuna prendo i vicini connessi
    def addedges2(self):
        self._grafo.clear_edges()
        for u in self._fermate:
            for conn in DAO.getvicini(u):
                v = self._idMapFermate[conn.id_stazA]
                self._grafo.add_edge(u,v)

    def addedges3(self):
        self._grafo.clear_edges()
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