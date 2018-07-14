class Heap:
    """ A min heap because it is lovely """

    def __init__(self):
        self.pq = [None] # lefts a dummy slot open to use 1 based index

    def swap(m, n):
        self.pq[m], self.pq[n] = self.pq[n], self.pq[m]

    def parent(item_idx):
        if item_idx == 1:
            return -1
        else:
            return item_idx // 2

    def young_child(item_idx):
        return item_idx * 2

    def old_child(item_idx):
        return item_idx * 2 + 1

    def insert(item):
        self.pq.append(item)
        item_idx = len(self.pq) - 1
        self.bubble_up(item_idx)

    def bubble_up(item_idx):
        parent_idx = self.parent(item_idx)
        if parent_idx == -1:
            return  # at root

        if self.pq[parent_idx] > self.pq[item_idx]:
            self.swap(parent_idx, item_idx)
            self.bubble_up(parent_idx)

    def extract_min(self):
        if len(self.pq) <=1:
            raise IndexError

        min_val = self.pq[1]
        self.pq[1] = self.pq.pop()
        self.bubble_down(1)

        return min_val

    def bubble_down(p):
        min_idx = p
        c1 = self.young_child(p)
        c2 = self.old_child(p)

        for c in (c1, c2):
            if c < len(self.pq):
                if self.pq[min_idx] > self.pq[c]:
                    min_idx = c

        if min_idx != p:
            self.swap(p, min_idx)
            self.bubble_down(min_idx)

    def compare(k, x, idx = 1):
        """ Is the kth smallest item in the heap greater than or euql to x
        Returns
            k if none >= x
            0 if there are enogh items that >= x
            something in between if items are exhausted
        """
        if k < 0 or i > len(self.pq):
            return k

        if self.pq[idx] < x:
            k = self.compare(k-1, x, self.young_child(idx))
            k = self.compare(k, x, self.old_child(idx))
        return k
