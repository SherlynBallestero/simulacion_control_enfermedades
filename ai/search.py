import heapq
from simulation.enviroment.graph import Graph, Node

def heuristic(node1:Node, node2:Node):
    '''
    Calcular la distancia de Manhattan entre dos puntos
    '''
    return  abs(node1.id[0] - node2.id[0]) + abs(node1.id[1] - node2.id[1])

def a_star(graph: Graph, start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == goal:
            break

        for next in graph.get_neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(graph.nodes[goal], graph.nodes[next])
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current
    
    return came_from, cost_so_far


