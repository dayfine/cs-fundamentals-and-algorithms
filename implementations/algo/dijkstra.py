# https://www.redblobgames.com/pathfinding/a-star/introduction.html

from queue import PriorityQueue


class graph:
    def get_neighbours(node):
        pass

    def cost(node, another_node):
        pass


def Dijkstra(start, goal, graph):
    frontier = PriorityQueue()
    frontier.put(start, 0)

    come_from = {}
    come_from[start] = None
    cost = {}
    cost[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.get_neighbours(current):
            new_cost = cost[current] + graph.cost(current, next)
            if next not in cost or new_cost < cost[next]:
                cost[next] = new_cost
                frontier.put(next, new_cost)
                come_from[next] = current
