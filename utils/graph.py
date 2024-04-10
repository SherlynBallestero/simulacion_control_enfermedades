from typing import Tuple, Hashable
import random

class Node:
    """
    Class representing a node in a graph.

    Attributes:
    - value: Value or information associated with the node.
    - name: Unique identifier for the node.
    """

    def __init__(self, id: Hashable =None)-> None:
        """
        Initializes a new node.

        Parameters:
        - value: Value or information associated with the node.
        - name: Unique identifier for the node.
        """
        self.id: int = id

    def __str__(self):
        """
        Returns a string representation of the node.

        Returns:
        - A string representing the node.
        """
        return f"Node({self.id})"

    def __repr__(self):
        """
        Returns a string representation of the node for use in the interpreter.

        Returns:
        - A string representing the node.
        """
        return self.__str__()

class Graph:
    """
    Class representing a graph.

    Attributes:
    - graph: Dictionary representing the graph, where keys are node names
              and values are lists of names of nodes connected to the key node.
    """

    def __init__(self)-> None:
        """
        Initializes a new graph.
        """
        self.nodes: dict[Hashable, Node] = {}
        self.edges: dict[Tuple[Hashable,Hashable], float] = {}

    def add_node(self, node:Node)-> None:
        """
        Adds a node to the graph.

        Parameters:
        - node: Node to add to the graph.
        """
        if node.id not in self.nodes:
            self.nodes[node.id] = node

    def add_edge(self, node1:int, node2:int, cost: float)-> Tuple[int, int]:
        """
        Adds an edge between two nodes in the graph.

        Parameters:
        - node1: First node of the edge.
        - node2: Second node of the edge.
        """
        if node1 in self.nodes and node2 in self.nodes:
            self.edges[(node1, node2)] = cost
            return (node1, node2)
        else:
            raise ValueError("Both nodes must be in the graph")

    def get_neighbors(self, node:int):
        neighbors = []
        for edge in self.edges:
            if node == edge[0]:
                if edge[1] not in neighbors:
                    neighbors.append(edge[1])
            if node == edge[1]:
                if edge[0] not in neighbors:
                    neighbors.append(edge[0])
        return neighbors
    
    def remove_node(self, node:int)->int:
        """
        Removes a node from the graph.

        Parameters:
        - node: Node to remove from the graph.
        """
        if node in self.nodes:
            return_node = self.nodes[node]
            del self.nodes[node]
            for edge in self.edges:
                if node in edge:
                    self.edges.remove(edge)
            return return_node
        else:
            raise ValueError("Node not in the graph")

    def remove_edge(self, node1:int, node2:int)-> Tuple[int,int]:
        """
        Removes an edge between two nodes in the graph.

        Parameters:
        - node1: First node of the edge.
        - node2: Second node of the edge.
        """
        for edge in self.add_edge:
            if node1 in edge and node2 in edge:
                del edge
                break
            else:
                raise ValueError("Both nodes must be in the same edge")

    def get_nodes(self) -> dict[int, Node]:
        """
        Returns a list of all nodes in the graph.

        Returns:
        - A list of nodes.
        """
        return self.nodes

    def get_edges(self)->list[Tuple[int,int]]:
        """
        Returns a list of all edges in the graph.

        Returns:
        - A list of edges.
        """
        return self.edges

    def get_random_node(self)-> Node:
        return random.choice(self.nodes(self))
    
    def __str__(self):
        """
        Returns a string representation of the graph.

        Returns:
        - A string representing the graph.
        """
        return str(self.nodes,self.edges)
    
    def cost(self, from_node_id, to_node_id):
        return self.edges.get((from_node_id, to_node_id), float('inf'))
