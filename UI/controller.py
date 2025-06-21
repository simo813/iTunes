import flet as ft
import networkx as nx
from model.album import Album


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.view = view
        # the model, which implements the logic of the program and holds the data
        self.model = model

    def handleCreaGrafo(self, e):
        if self.view._txtInDurata.value is not None:
            self.view.txt_result.clean()
            self.view.reset_dropdown_album()
            duration = int(self.view._txtInDurata.value)
            self.model.createGraph(duration)
            graph = self.model.graph
            listNodes = graph.nodes()
            for node in listNodes:
                self.view.ddAlbum.options.append(ft.dropdown.Option(key=node.AlbumId, text=node.title))
            self.view.txt_result.controls.append(ft.Text(
                f"Grafo creato!\n"
                f"Il numero di vertici è {graph.number_of_nodes()}\n"
                f"Il numero di archi è {graph.number_of_edges()}\n"))
        else:
            self.view.txt_result.controls.append(ft.Text(
                f"Inserisci i valori"))
        self.view.update_page()


    def handleAnalisiComp(self, e):
        if self.view.ddAlbumValue is not None:
            self.view.txt_result.clean()
            graph = self.model.graph
            print(f"stampa {self.view.ddAlbumValue}")
            selectedAlbum = self.model.idMapAlbum[int(self.view.ddAlbumValue)]
            connectedComponents = list(nx.connected_components(graph))
            for component in connectedComponents:
                if selectedAlbum in component:
                    sum = 0
                    self.view.txt_result.controls.append(ft.Text(
                        f"Dimensione componente connessa {len(component)}\n"))
                    for node in component:
                        sum += node.duration
                    self.view.txt_result.controls.append(ft.Text(
                        f"Durata album {sum}\n"))
        else:
            self.view.txt_result.controls.append(ft.Text(
                f"Inserisci i valori"))
        self.view.update_page()


    def handleGetSetAlbum(self, e):
        if self.view._txtInSoglia.value is not None:
            self.view.txt_result.clean()
            dTot = int(self.view._txtInSoglia.value)
            selectedAlbum = self.model.idMapAlbum[int(self.view.ddAlbumValue)]
            optPath, optPathDuration = self.model.getOptPath(selectedAlbum, dTot)
            for node in optPath:
                self.view.txt_result.controls.append(ft.Text(
                    f"{node.__str__()}\n"))
        else:
            self.view.txt_result.controls.append(ft.Text(
                f"Inserisci i valori corretti"))
        self.view.update_page()



