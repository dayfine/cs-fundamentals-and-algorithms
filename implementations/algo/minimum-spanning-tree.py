class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append(u, v, w)

    def find(self, ids, p):
        while p != ids[p]:
            ids[p] = ids[ids[p]]
            p = ids[p]
        return p

    def union(self, ids, ranks, x, y):
        X = self.find(ids, x)
        Y = self.find(ids, y)

        if ranks[X] < ranks[Y]:
            ids[X] = Y
        elif ranks[X] > ranks[Y]:
            ids[Y] = X
        else:
            ranks[X] += 1
            ids[Y] = X

    def minimum_spanning_tree(self):
        result = []

        # sorting by weight
        self.graph.sort(key=lambda item: item[2])

        ids, ranks = [None] * self.num_vertices, [0] * self.num_vertices

        idx, edge = 0, 0

        while edge < self.num_vertices - 1:
            u, v, w = self.graph[idx]
            idx += 1
            x = self.find(ids, u)
            y = self.find(ids, v)

            if x != y:
                edge = edge + 1
                result.append(self.graph[idx])
                self.union(ids, ranks, x, y)

        return result

g = Graph()
g.addEdge(0, 1, 10)
g.addEdge(0, 2, 6)
g.addEdge(0, 3, 5)
g.addEdge(1, 3, 15)
g.addEdge(2, 3, 4)




