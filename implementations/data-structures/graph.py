class Graph:
    def __init__(self, vertices):
        self.length = len(vertices)
        self.graph = list([0]*self.list_len for i in range(self.list_len))
