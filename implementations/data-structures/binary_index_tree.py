class BIT():

    def __init__(self, arr):
        """ Create tree with a dummy head node"""
        self.size = len(arr) + 1
        self.tree = [0] * self.size
        for idx, val in enumerate(arr):
            self.update(self, idx, val)

    def readCumu(self, idx):
        # note this is internal idx
        # which is one larger than arr index
        res = 0

        while idx > 0:
            res += self.tree[idx]
            idx -= (idx & -idx)
        return res

    def update(self, idx, val):
        # val will be added to element at idx
        while idx < self.size:
            self.tree[idx] += val
            idx += (idx & -idx)

    def readSingle(self, idx):
        res = self.tree[idx]
        if idx > 0:
            z = idx - (idx & -idx)
            idx -= 1

            while z != idx:
                res -= self.tree[idx]
                idx -= (idx & -idx)

        return res

    def scale(self, factor):
        self.tree = [ val * factor for val in self.tree ]



class BIT2D():
    """
    Note all methods expect the indices to be indices in the tree,
    i.e. it would be one larger than the respective indices for the matrix
    """
    def __init__(self, matrix):
        self.maxX = len(matrix) + 1
        self.maxY = len(matrix[0]) + 1
        self.tree = [[0] * self.maxY for _ in range(self.maxX)]
        self.matrix = matrix

        for i in range(1, self.maxX):
            for j in range(1, self.maxY):
                self.update(i, j, matrix[i-1][j-1])

    def read(self, x, y):
        res = 0
        while x > 0:
            res += self.readY(x, y)
            x -= (x & -x)
        return res


    def readY(self, x, y):
        res = 0
        while y > 0:
            res += self.tree[x][y]
            y -= (y & -y)
        return res


    def update(self, x, y, val):
        while x < self.maxX:
            self.updateY(x, y, val)
            x += (x & -x)

    def updateY(self, x, y, val):
        while y < self.maxX:
            self.tree[x][y] += val
            y += (y & -y)

