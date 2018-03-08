from collections import namedtuple
from operator import itemgetter
from pprint import pformat


class KdTree():
    def __init__(self, points, depth=0):
        k = len(points[0])
        self.axis = depth % k

        points.sort(key=itemgetter(self.axis))
        median = len(points) // 2

        self.location = points[median]
        if median == 0:
            self.left = None
        else:
            self.left = KdTree(points[:median], depth + 1)

        if median == len(points) - 1:
            self.right = None
        else:
            self.right = KdTree(points[median + 1:], depth + 1)

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.location) + "\n"
        if self.left is not None:
            ret += self.left.__str__(level+1)
        if self.right is not None:
            ret += self.right.__str__(level+1)
        return ret

    def nearest_neigbour(self, point):
        best_pt, best_sq_dist = None, float('inf')

        def nns(node, point, best_pt, best_sq_dist):
            if node is None:
                return
            print(node, node.left, node.right)
            if node.left is None and node.right is None:
                sq_dist = square_dist(point, node.location)
                if sq_dist < best_sq_dist:
                    best_pt, best_sq_dist = point, sq_dist
                    return best_pt

            axis = node.axis
            left_first = point[axis] <= node.location[axis]

            if left_first:
                if point[axis] - best_sq_dist <= node.location[axis]:
                    if node.left is not None:
                        nns(node.left, point, best_pt, best_sq_dist)
                elif point[axis] + best_sq_dist >= node.location[axis]:
                    nns(node.right, point, best_pt, best_sq_dist)
            else:
                if point[axis] + best_sq_dist >= node.location[axis]:
                    nns(node.right, point, best_pt, best_sq_dist)
                elif point[axis] - best_sq_dist <= node.location[axis]:
                    nns(node.left, point, best_pt, best_sq_dist)
        return nns(self, point, best_pt, best_sq_dist)

point_list = [(2,3), (5,4), (9,6), (4,7), (8,1), (7,2)]
kd_tree = KdTree(point_list)
print(kd_tree)
# print(kd_tree.nearest_neigbour([7.5, 1.6]))

