import heapq
from simulation.enviroment.graph import Graph
from simulation.enviroment.map import Terrain
import math
import sys
from collections import  deque

def heuristic(node, node2):
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


















class Problem(object):
    """The abstract class for a formal problem. A new domain subclasses this,
    overriding `actions` and `results`, and perhaps other methods.
    The default heuristic is 0 and the default action cost is 1 for all states.
    When you create an instance of a subclass, specify `initial`, and `goal` states 
    (or give an `is_goal` method) and perhaps other keyword args for the subclass."""

    def __init__(self, initial=None, goal=None, **kwds): 
        self.__dict__.update(initial=initial, goal=goal, **kwds) 

    def actions(self, state):        raise NotImplementedError
    def result(self, state, action): raise NotImplementedError
    def is_goal(self, state):        return state == self.goal
    def action_cost(self, s, a, s1): return 1
    def h(self, node):               return 0

    def __str__(self):
        return '{}({!r}, {!r})'.format(
            type(self).__name__, self.initial, self.goal)


class AgentPathProblem(Problem):
    def __init__(self, initial, goal, map, path_type = 'shortest_path'):
        self.initial, self.goal, self.map, self.path_type = initial, goal, map, path_type

    def actions(self, state):
        return [self.map[node_id] for node_id in self.map.get_neighbors(state.id)]
    
    def action_cost(self, s, a, s1): 
        if self.path_type == 'shortest_path':
            return 1
        elif self.path_type == 'minimum_contact_path':
            self.calculate_contact_danger(s1)

    def result(self, state, action):
        return action
    
    def manhattan_h(self, node):
        return  abs(node.state.addr[0] - self.goal.addr[0]) + abs(node.state.addr[1] - self.goal.addr[1])

    def calculate_contact_danger(self, node):
        # calculate contact danger based on capacity status
        contact_danger = {
            'low': 1, 'medium': 2, 'high': 3, 'very_high': 4
        }
        if node.state.capacity_status == 'unknown':
            total = 0
            for neighbor in self.map.get_neighbors(node.state.id):
                if self.map[neighbor].capacity_status != 'unknown':
                    total += contact_danger[self.map[neighbor].capacity_status]
            contact_val = total/ len(self.map.get_neighbors(node.state.id))
            #change the state so capacity status corresponds to the 
            node.state.capacity_status = 'low' if contact_val < 1.5 else 'medium' if contact_val < 2.5 else 'high' if contact_val < 3.5 else 'very_high'
        return contact_danger[node.state.capacity_status]

    def minimum_contact_h(self, node):# TODO: define a heuristic of minimum cost path
        return self.calculate_contact_danger(node) + self.manhattan_h(node)

    def h(self, node): 
        if self.path_type == 'shortest_path':
            return self.manhattan_h(node)
        elif self.path_type == 'minimum_contact_path':
            return self.minimum_contact_h(node)


class Node:
    "A Node in a search tree."
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.__dict__.update(state=state, parent=parent, action=action, path_cost=path_cost)

    def __repr__(self): return '<{}>'.format(self.state)
    def __len__(self): return 0 if self.parent is None else (1 + len(self.parent))
    def __lt__(self, other): return self.path_cost < other.path_cost


failure = Node('failure', path_cost=math.inf) # Indicates an algorithm couldn't find a solution.
cutoff  = Node('cutoff',  path_cost=math.inf) # Indicates iterative deepening search was cut off.


def expand(problem, node):
    "Expand a node, generating the children nodes."
    s = node.state
    for action in problem.actions(s):
        s1 = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s1)
        yield Node(s1, node, action, cost)


def path_actions(node):
    "The sequence of actions to get to this node."
    if node.parent is None:
        return []  
    return path_actions(node.parent) + [node.action]


def path_states(node):
    "The sequence of states to get to this node."
    if node in (cutoff, failure, None): 
        return []
    return path_states(node.parent) + [node.state.id]


FIFOQueue = deque


LIFOQueue = list


class PriorityQueue:
    """A queue in which the item with minimum f(item) is always popped first."""

    def __init__(self, items=(), key=lambda x: x): 
        self.key = key
        self.items = [] # a heap of (score, item) pairs
        for item in items:
            self.add(item)
         
    def add(self, item):
        """Add item to the queuez."""
        pair = (self.key(item), item)
        heapq.heappush(self.items, pair)

    def pop(self):
        """Pop and return the item with min f(item) value."""
        return heapq.heappop(self.items)[1]
    
    def top(self): return self.items[0][1]

    def __len__(self): return len(self.items)


def best_first_search(problem, f):
    "Search nodes with minimum f(node) value first."
    node = Node(problem.initial)
    frontier = PriorityQueue([node], key=f)
    reached = {problem.initial: node}
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.add(child)
    return failure


def best_first_tree_search(problem, f):
    "A version of best_first_search without the `reached` table."
    frontier = PriorityQueue([Node(problem.initial)], key=f)
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            if not is_cycle(child):
                frontier.add(child)
    return failure

def shortest_path_g(n): return 1
def minimum_contact_path_g(n): return 1
def g(n): return n.path_cost

def astar_search(problem, h=None, g_selection=None):
    """Search nodes with minimum f(n) = g(n) + h(n)."""
    h = h or problem.h
    if g_selection == 'shortest_path':
        return best_first_search(problem, f=lambda n: shortest_path_g(n) + h(n))
    if g_selection == 'minimum_contact_path':
        return best_first_search(problem, f=lambda n: minimum_contact_path_g(n) + h(n))
    else:
        return best_first_search(problem, f = lambda n: g(n) + h(n))

def astar_tree_search(problem, h=None):
    """Search nodes with minimum f(n) = g(n) + h(n), with no `reached` table."""
    h = h or problem.h
    return best_first_tree_search(problem, f=lambda n: g(n) + h(n))


def weighted_astar_search(problem, h=None, weight=1.4):
    """Search nodes with minimum f(n) = g(n) + weight * h(n)."""
    h = h or problem.h
    return best_first_search(problem, f=lambda n: g(n) + weight * h(n))


def greedy_bfs(problem, h=None):
    """Search nodes with minimum h(n)."""
    h = h or problem.h
    return best_first_search(problem, f=h)


def uniform_cost_search(problem):
    "Search nodes with minimum path cost first."
    return best_first_search(problem, f=g)


def breadth_first_bfs(problem):
    "Search shallowest nodes in the search tree first; using best-first."
    return best_first_search(problem, f=len)


def depth_first_bfs(problem):
    "Search deepest nodes in the search tree first; using best-first."
    return best_first_search(problem, f=lambda n: -len(n))


def is_cycle(node, k=30):
    "Does this node form a cycle of length k or less?"
    def find_cycle(ancestor, k):
        return (ancestor is not None and k > 0 and
                (ancestor.state == node.state or find_cycle(ancestor.parent, k - 1)))
    return find_cycle(node.parent, k)


def breadth_first_search(problem):
    "Search shallowest nodes in the search tree first."
    node = Node(problem.initial)
    if problem.is_goal(problem.initial):
        return node
    frontier = FIFOQueue([node])
    reached = {problem.initial}
    while frontier:
        node = frontier.pop()
        for child in expand(problem, node):
            s = child.state
            if problem.is_goal(s):
                return child
            if s not in reached:
                reached.add(s)
                frontier.appendleft(child)
    return failure


def iterative_deepening_search(problem):
    "Do depth-limited search with increasing depth limits."
    for limit in range(1, sys.maxsize):
        result = depth_limited_search(problem, limit)
        if result != cutoff:
            return result


def depth_limited_search(problem, limit=10):
    "Search deepest nodes in the search tree first."
    frontier = LIFOQueue([Node(problem.initial)])
    result = failure
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        elif len(node) >= limit:
            result = cutoff
        elif not is_cycle(node):
            for child in expand(problem, node):
                frontier.append(child)
    return result


def depth_first_recursive_search(problem, node=None):
    if node is None: 
        node = Node(problem.initial)
    if problem.is_goal(node.state):
        return node
    elif is_cycle(node):
        return failure
    else:
        for child in expand(problem, node):
            result = depth_first_recursive_search(problem, child)
            if result:
                return result
        return failure

