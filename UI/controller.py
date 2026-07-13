import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDStore(self):
        allStores = self._model.getAllStores()

        for y in allStores:
            anno_str = str(y)
            #anno_str = str(y)  # Convertiamo l'intero in stringa (es: "2005")
            # Creiamo l'opzione Flet reale e facciamo l'append
            self._view._ddStore.options.append(ft.dropdown.Option(key=anno_str,text=anno_str))

        self._view.update_page()

    def handleCreaGrafo(self, e):
        self._model.buildGraph(self._view._ddStore.value, self._view._txtIntK.value)
        Nnodes, Nedges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato. "
                                                      f"Il grafo contiene {Nnodes} nodi e {Nedges} archi"))
        top5 = self._model.getTop5Archi()
        #self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Archi di peso maggiore: "))

        for arco in top5:
            self._view.txt_result.controls.append(ft.Text(f"{arco[0]}-->{arco[1]} (peso: {arco[2]["weight"]})"))
        self._view.update_page()

    def fillDDNodes(self):
       # self._view.txt_result.controls.clear()
        allNodes= self._model.getAllNodes()
        self._view._ddNode.options.clear()

        for y in allNodes:
            id_ordine_str = str(y.order_id)
            # Creiamo l'opzione Flet reale e facciamo l'append
            self._view._ddStore.options.append(ft.dropdown.Option(key=id_ordine_str, text=str(y)))

        self._view.update_page()


    def handleCerca(self, e):
        self._view.txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._view.create_alert("Creare prima il grafo.")


    def handleRicorsione(self, e):
        self._view.txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._view.create_alert("Creare prima il grafo.")
