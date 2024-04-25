from simulation.enviroment.graph import Graph
from simulation.enviroment.sim_nodes import *
from typing import Dict, List, Tuple, Union

class Terrain:
    """
    Class that represents the terrain of the simulation, including blocks, workspaces, recreational places, hospitals, bus stops, and houses.
    """
    def __init__(self):
        """
        Initializes the terrain with an empty graph and empty lists for the different types of nodes.
        """
        self.graph: Graph = Graph()
        self.works: List[Workspace] = []
        self.recreational: List[PublicPlace] = []
        self.hospitals: List[Hospital] = []
        self.bus_stops: List[BusStop] = []
        self.houses: List[HouseNode] = []
        self.nodes_by_addrs: Dict[Tuple, List[SimNode]] = {}
        
    def add_block(self, addr: Tuple, capacity: int):
        """
        Adds a block to the terrain with a given address and capacity.
        
        Args:
            addr (Tuple): Address of the block.
            capacity (int): Capacity of the block.
        """
        id_list = list(self.graph.nodes.keys())
        last_id = id_list[-1] if id_list else 0
        node = BlockNode(capacity, last_id+1, addr)
        self._add_node(node)
    
    def add_work(self, addr: Tuple, capacity: int, opening_hours: int = 8, closing_hours: int = 18):
        """
        Adds a workspace to the terrain with a given address and capacity.
        
        Args:
            addr (Tuple): Address of the workspace.
            capacity (int): Capacity of the workspace.
        """
        id_list = list(self.graph.nodes.keys())
        last_id = id_list[-1] if id_list else 0
        for node in self.graph.nodes.values():
            if isinstance(node, BlockNode) and node.addr == addr:
                w_node = Workspace(capacity, last_id+1, addr, opening_hours, closing_hours)
                self.works.append(w_node)
                self._add_node(w_node)
                self.add_edge(node.id, w_node.id)
                break
    
    def add_house(self, addr: Tuple, capacity: int):
        """
        Adds a house to the terrain with a given address and capacity.
        
        Args:
            addr (Tuple): Address of the house.
            capacity (int): Capacity of the house.
        """
        id_list = list(self.graph.nodes.keys())
        last_id = id_list[-1] if id_list else 0
        for node in self.graph.nodes.values():
            if isinstance(node, BlockNode) and node.addr == addr:
                w_node = HouseNode(capacity, last_id+1, addr)
                self.houses.append(w_node)
                self._add_node(w_node)
                self.add_edge(node.id, w_node.id)
                break
    
    def add_recreational(self, addr: Tuple, capacity: int, opening_hours: int = 19, closing_hours: int = 23):
        """
        Adds a recreational place to the terrain with a given address and capacity.
        
        Args:
            addr (Tuple): Address of the recreational place.
            capacity (int): Capacity of the recreational place.
        """
        id_list = list(self.graph.nodes.keys())
        last_id = id_list[-1] if id_list else 0
        for node in self.graph.nodes.values():
            if isinstance(node, BlockNode) and node.addr == addr:
                w_node = PublicPlace(capacity, last_id+1, addr, opening_hours, closing_hours)
                self.recreational.append(w_node.id)
                self._add_node(w_node)
                self.add_edge(node.id, w_node.id)
                break
    
    def add_hospital(self, addr: Tuple, capacity: int, opening_hours: int = 8, closing_hours: int = 18):
        """
        Adds a hospital to the terrain with a given address and capacity.
        
        Args:
            addr (Tuple): Address of the hospital.
            capacity (int): Capacity of the hospital.
        """
        id_list = list(self.graph.nodes.keys())
        last_id = id_list[-1] if id_list else 0
        for node in self.graph.nodes.values():
            if isinstance(node, BlockNode) and node.addr == addr:
                w_node = Hospital(capacity, last_id+1, addr, opening_hours, closing_hours)
                self.hospitals.append(w_node)
                self._add_node(w_node)
                self.add_edge(node.id, w_node.id)
                break
    
    def add_bus_stop(self, addr: Tuple, capacity: int):
        """
        Adds a bus stop to the terrain with a given address and capacity.
        
        Args:
            addr (Tuple): Address of the bus stop.
            capacity (int): Capacity of the bus stop.
        """
        id_list = list(self.graph.nodes.keys())
        last_id = id_list[-1] if id_list else 0
        for node in self.graph.nodes.values():
            if isinstance(node, BlockNode) and node.addr == addr:
                w_node = BusStop(capacity, last_id+1, addr)
                self.bus_stops.append(w_node.id)
                self._add_node(w_node)
                self.add_edge(node.id, w_node.id)
                break
    
    def add_edge(self, id1: int, id2: int):
        """
        Adds an edge between two nodes in the terrain's graph.
        
        Args:
            id1 (int): ID of the first node.
            id2 (int): ID of the second node.
        """
        self.graph.add_edge(id1, id2, 1)
        
    def _add_node(self, node: SimNode):
        """
        Adds a node to the terrain's graph and updates the dictionary of nodes by addresses.
        
        Args:
            node (SimNode): Node to add.
        """
        if node.addr in self.nodes_by_addrs.keys():
            self.nodes_by_addrs[node.addr].append(node)
        else:
            self.nodes_by_addrs[node.addr] = [node]
                
        self.graph.add_node(node)
        
    def __getitem__(self, index: Union[Tuple, int]):
        """
        Gets a node or a list of nodes by their address or ID.
        
        Args:
            index (Union[Tuple, int]): Address or ID of the node.
        """
        if isinstance(index, tuple):
            return self.nodes_by_addrs[index]
        else:
            return self.graph.nodes[index]
        
    def keys(self):
        """
        Gets the addresses of all nodes in the terrain.
        
        Returns:
            KeysView[Tuple]: View of the node addresses.
        """
        return self.graph.nodes.keys()
