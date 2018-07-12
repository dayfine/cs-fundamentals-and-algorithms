class UnionFind():

    def __init__(n):
        self._id = [None] * n
        self._size = [1] * n
        self.count = 0

    def add(self, idx):
        self._id[idx] = idx
        self.count += 1

    def find(self, p):
        while p != self._id[p]:
            self._id[p] = self._id[self._id[p]]
            p = self._id[p]
        return p

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def union(self, p, q):
        P, Q = self.find(p), self.find(q)

        if P == Q:
            return

        if self._size(P)<self._size[Q]:
            P, Q = Q, P

        self._id[Q] = P
        self._size[P]+=self._size[Q]
