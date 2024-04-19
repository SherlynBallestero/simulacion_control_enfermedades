import heapq
from simulation.enviroment.graph import Graph, Node
from simulation.enviroment.map import Terrain

def heuristic(node1:Node, node2:Node):
    '''
    Calcular la distancia de Manhattan entre dos puntos
    '''
    return  abs(node1.addr[0] - node2.addr[0]) + abs(node1.addr[1] - node2.addr[1])

def a_star(terrain: Terrain, start, goal): 
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

        for next in terrain.graph.get_neighbors(current):
            new_cost = cost_so_far[current] + terrain.graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(terrain.graph.nodes[goal], terrain.graph.nodes[next])
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current

    return came_from, cost_so_far



def bfs(graph, start, goal):
    visited = set()
    queue = [(start, [start])]

    while queue:
        (vertex, path) = queue.pop(0)
        if vertex not in visited:
            if vertex == goal:
                return path
            visited.add(vertex)
            for neighbor in graph.graph.get_neighbors(vertex):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

    return None