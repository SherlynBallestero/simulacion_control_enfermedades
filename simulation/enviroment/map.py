from utils.graph import Graph
from simulation.utils.sim_nodes import *
from typing import Dict

class Terrain:
    def __init__(self):
        self.graph:Graph = Graph()
        self.works: list[Workspace] = []
        self.recreational: list[PublicPlace] = []
        self.hospitals: list[Hospital] = []
        self.bus_stops: list[BusStop] = []
        self.houses: list[HouseNode] = []
        self.nodes_by_addrs: Dict[Tuple,list[SimNode]] = {}
        
    def add_block(self, addr, capacity):
        id_list = list(self.graph.nodes.keys())
        last_id = id_list[-1] if id_list else 0
        node = BlockNode(capacity, last_id+1, addr)
        self._add_node(node)
    
    def add_work(self, addr, capacity):
        id_list = list(self.graph.nodes.keys())
        last_id = id_list[-1] if id_list else 0
        for node in self.graph.nodes.values():
            if isinstance(node,BlockNode) and node.addr == addr:
                w_node = Workspace(capacity, last_id+1, addr)
                self.works.append(w_node.id)
                self._add_node(w_node)
                self.add_edge(node.id, w_node.id)
                break
    
    def add_house(self, addr, capacity):
        id_list = list(self.graph.nodes.keys())
        last_id = id_list[-1] if id_list else 0
        for node in self.graph.nodes.values():
            if isinstance(node,BlockNode) and node.addr == addr:
                w_node = HouseNode(capacity, last_id+1, addr)
                self.houses.append(w_node.id)
                self._add_node(w_node)
                self.add_edge(node.id, w_node.id)
                break
    
    def add_recreational(self, addr, capacity):
        id_list = list(self.graph.nodes.keys())
        last_id = id_list[-1] if id_list else 0
        for node in self.graph.nodes.values():
            if isinstance(node,BlockNode) and node.addr == addr:
                w_node = PublicPlace(capacity, last_id+1, addr)
                self.recreational.append(w_node.id)
                self._add_node(w_node)
                self.add_edge(node.id, w_node.id)
                break
    
    def add_hospital(self, addr, capacity):
        id_list = list(self.graph.nodes.keys())
        last_id = id_list[-1] if id_list else 0
        for node in self.graph.nodes.values():
            if isinstance(node,BlockNode) and node.addr == addr:
                w_node = Hospital(capacity, last_id+1, addr)
                self.hospitals.append(w_node.id)
                self._add_node(w_node)
                self.add_edge(node.id, w_node.id)
                break
    
    def add_bus_stop(self, addr, capacity):
        id_list = list(self.graph.nodes.keys())
        last_id = id_list[-1] if id_list else 0
        for node in self.graph.nodes.values():
            if isinstance(node,BlockNode) and node.addr == addr:
                w_node = BusStop(capacity, last_id+1, addr)
                self.bus_stops.append(w_node.id)
                self._add_node(w_node)
                self.add_edge(node.id, w_node.id)
                break
    
    def add_edge(self, id1, id2):
        self.graph.add_edge(id1, id2, 1)
        
    def _add_node(self,node: SimNode):
        if node.addr in self.nodes_by_addrs.keys():
            self.nodes_by_addrs[node.addr].append(node)
        else:
            self.nodes_by_addrs[node.addr] = [node]
                
        self.graph.add_node(node)
        
    def __getitem__(self, index):
        if isinstance(index, tuple):
            return self.nodes_by_addrs[index]
        else:
            return self.graph.nodes[index]
        
    def keys(self):
        return self.graph.nodes.keys()
        
        