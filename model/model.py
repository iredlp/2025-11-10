import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()  # grafo semplice ORIENTATO
        self._idMapO = {}

    def buildGraph(self, store, k):
        # svuoto il grafo
        self._graph.clear()
        self._stores = DAO.getAllNodes(store)

        for d in self._stores :
            self._idMapO[d.order_id] = d

        # aggiungo i nodi al grafo
        self._graph.add_nodes_from(self._stores)

        edges = DAO.getAllEdges(store, k, self._idMapO)
        for e in edges:
            self._graph.add_edge(e.o1, e.o2, weight=e.peso)

    def getTop5Archi(self):
        return sorted(self._graph.edges(data=True),
                      key=lambda x: x[2]["weight"], reverse=True)[:5]

    def getAllStores(self):
        return DAO.getAllStores()

    def getAllNodes(self):
        return list(self._graph.nodes())

    def getNumNodi(self):
        return len(self._graph.nodes)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getCamminoMassimo(self, nodo_partenza):
        # Inizializziamo le strutture per salvare il risultato migliore
        self._best_cammino = []
        self._best_peso_totale = 0

        # Iniziamo la ricorsione partendo dal nodo scelto
        # Il cammino parziale all'inizio contiene solo il nodo di partenza
        cammino_parziale = [nodo_partenza]

        self._ricorsione(cammino_parziale, 0)

        return self._best_cammino, self._best_peso_totale

    def _ricorsione(self, parziale, peso_accumulato):
        # 1. Caso terminale / Controllo Soluzione Migliore:
        # Ogni volta che entriamo nella ricorsione, controlliamo se il cammino attuale
        # ha un peso maggiore di quello massimo trovato finora.
        if peso_accumulato > self._best_peso_totale:
            self._best_peso_totale = peso_accumulato
            self._best_cammino = list(parziale)  # Facciamo una copia della lista

        # 2. Esplorazione dei vicini (Passo Generativo):
        # Prendiamo l'ultimo nodo inserito nel cammino parziale
        nodo_corrente = parziale[-1]

        # Cicliamo su tutti i successori (i nodi vicini raggiungibili tramite un arco uscente)
        for vicino in self._graph.successors(nodo_corrente):

            # Condizione di validità: il nodo non deve essere già stato visitato
            # (Nel nostro grafo aciclico temporale è quasi impossibile, ma l'if va messo per rigore)
            if vicino not in parziale:
                # Recuperiamo il peso dell'arco tra nodo_corrente e vicino
                peso_arco = self._graph[nodo_corrente][vicino]['weight']

                # --- BACKTRACKING ---
                # Aggiungiamo il vicino alla soluzione parziale
                parziale.append(vicino)

                # Lanciamo la ricorsione aggiornando il peso accumulato
                self._ricorsione(parziale, peso_accumulato + peso_arco)

                # Togliamo il vicino (backtrack) per esplorare le altre strade nei cicli successivi
                parziale.pop()