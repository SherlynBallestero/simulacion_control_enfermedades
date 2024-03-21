
class Node:
    """
    Class representing a node in a graph.

    Attributes:
    - value: Value or information associated with the node.
    - name: Unique identifier for the node.
    """

    def __init__(self, value=None, name=None):
        """
        Initializes a new node.

        Parameters:
        - value: Value or information associated with the node.
        - name: Unique identifier for the node.
        """
        self.value = value
        self.name = name

    def __str__(self):
        """
        Returns a string representation of the node.

        Returns:
        - A string representing the node.
        """
        return f"Node({self.name}, {self.value})"

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

    def __init__(self):
        """
        Initializes a new graph.
        """
        self.graph = {}

    def add_node(self, node):
        """
        Adds a node to the graph.

        Parameters:
        - node: Node to add to the graph.
        """
        if node.name not in self.graph:
            self.graph[node.name] = []

    def add_edge(self, node1, node2):
        """
        Adds an edge between two nodes in the graph.

        Parameters:
        - node1: First node of the edge.
        - node2: Second node of the edge.
        """
        if node1.name in self.graph and node2.name in self.graph:
            self.graph[node1.name].append(node2.name)
            self.graph[node2.name].append(node1.name)
        else:
            raise ValueError("Both nodes must be in the graph")

    def remove_node(self, node):
        """
        Removes a node from the graph.

        Parameters:
        - node: Node to remove from the graph.
        """
        if node.name in self.graph:
            del self.graph[node.name]
            for key in self.graph:
                if node.name in self.graph[key]:
                    self.graph[key].remove(node.name)
        else:
            raise ValueError("Node not in the graph")

    def remove_edge(self, node1, node2):
        """
        Removes an edge between two nodes in the graph.

        Parameters:
        - node1: First node of the edge.
        - node2: Second node of the edge.
        """
        if node1.name in self.graph and node2.name in self.graph:
            if node2.name in self.graph[node1.name]:
                self.graph[node1.name].remove(node2.name)
            if node1.name in self.graph[node2.name]:
                self.graph[node2.name].remove(node1.name)
        else:
            raise ValueError("Both nodes must be in the graph")

    def get_nodes(self):
        """
        Returns a list of all nodes in the graph.

        Returns:
        - A list of nodes.
        """
        return list(self.graph.keys())

    def get_edges(self):
        """
        Returns a list of all edges in the graph.

        Returns:
        - A list of edges.
        """
        edges = []
        for node in self.graph:
            for neighbor in self.graph[node]:
                if {node, neighbor} not in edges:
                    edges.append({node, neighbor})
        return edges

    def __str__(self):
        """
        Returns a string representation of the graph.

        Returns:
        - A string representing the graph.
        """
        return str(self.graph)