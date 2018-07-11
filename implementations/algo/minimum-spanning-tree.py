"""
https://algs4.cs.princeton.edu/43mst/
https://www.wikiwand.com/en/Disjoint-set_data_structure
https://www.wikiwand.com/en/Kruskal%27s_algorithm
"""

class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    def find(self, ids, p):
        while p != ids[p]:
            ids[p] = ids[ids[p]]
            p = ids[p]
        return p

    def union(self, ids, sizes, x, y):
        X = self.find(ids, x)
        Y = self.find(ids, y)

        if X == Y:
            return

        if sizes[X] < sizes[Y]:
            X, Y = Y, X
        ids[Y] = X
        sizes[X] += sizes[Y]

    def minimum_spanning_tree(self):
        result = []

        # sorting by weight
        self.graph.sort(key=lambda item: item[2])

        ids, sizes = [], []
        for i in range(self.num_vertices):
            ids.append(i)
            sizes.append(1)

        idx, edge = 0, 0
        while edge < self.num_vertices - 1:
            u, v, w = self.graph[idx]
            idx += 1
            U = self.find(ids, u)
            V = self.find(ids, v)

            if U != V:
                edge = edge + 1
                result.append([u, v, w])
                print(result)
                self.union(ids, sizes, U, V)

        return result

g = Graph(4)
g.add_edge(0, 1, 10)
g.add_edge(0, 2, 6)
g.add_edge(0, 3, 5)
g.add_edge(1, 3, 15)
g.add_edge(2, 3, 4)

MST = g.minimum_spanning_tree()
print(MST)




