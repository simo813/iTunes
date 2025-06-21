import copy

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self.optPath = None
        self.optPathDuration = None
        self.DAO = DAO()
        self.graph = None
        self.idMapAlbum = {}


    def createGraph(self, duration):
        self.graph = nx.Graph()
        listNodes = self.DAO.getNodes(duration)
        for node in listNodes:
            self.idMapAlbum[node.AlbumId] = node
        self.graph.add_nodes_from(listNodes)
        for album1 in listNodes:
            for album2 in listNodes:
                if self.DAO.getEdge(album1.AlbumId, album2.AlbumId) > 0 and album1 != album2 and album1.AlbumId > album2.AlbumId:
                    self.graph.add_edge(album1, album2)


    def getOptPath(self, source, dTot):
        self.optPath = []
        self.optPathDuration = 0

        self.recursion(
            source=source,
            partial=[source],
            partialDuration=0,
            dTot = dTot
        )
        print("\nENTRATO\n")
        print(self.optPath)
        print(self.optPathDuration)
        print("\nFINE\n")

        return self.optPath, self.optPathDuration

    def recursion(self, source, partial, partialDuration, dTot):
        graph = self.graph

        if len(partial) > len(self.optPath):
            print("\n---------------------------------")
            print(partialDuration)
            self.optPathDuration = partialDuration
            self.optPath = copy.deepcopy(partial)


        for node in nx.node_connected_component(graph, source):
            if node not in partial:
                if (partialDuration + node.duration) <= dTot:
                    print("")
                    partial.append(node)
                    self.recursion(node, partial, partialDuration + node.duration, dTot)
                    print("NUOVA RICORSIONE\n")
                    partial.pop()





