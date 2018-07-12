# https://www.redblobgames.com/pathfinding/a-star/introduction.html

from queue import Queue


class graph:
    def get_neighbours(node):
        pass


def BFS(start, goal, graph):
    frontier = Queue()
    frontier.put(start)

    come_from = {}
    come_from[start] = None

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.get_neighbours(current):
            if next not in come_from:
                frontier.put(next)
                come_from[next] = current
