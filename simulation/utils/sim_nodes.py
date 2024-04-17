from utils.graph import Node
from typing import Hashable, Tuple, Callable, Any

class PerceptionNode(Node):
    def __init__(self, addr:Tuple[int, int], id: Hashable = None) -> None:
        super().__init__(id)
        self._node_name = "PerceptionNode"
        self.addr = addr

class CitizenPerceptionNode(PerceptionNode):
    def __init__(self, addr:Tuple[int, int], id: Hashable, node_type:str, capacity_status: str = 'unknown', information_source: str = 'perception') -> None:
        super().__init__(addr, id)
        self.capacity_status = capacity_status
        self.information_source = information_source
        self.node_type = node_type


class SimNode(Node):
    def __init__(self, capacity: int, id: Hashable, addr:Tuple[int, int], contact_rate: Callable = None):
        """
        Class representing the base node of the simulation

        Args:
            capacity (int): Represents the capacity of the node.
            id (int): The identifier of the node.
        """
        super().__init__(id)
        self.capacity = capacity
        self.agent_list = []
        self.addr = addr


    def __str__(self):
        agents = '\n\t'.join(self.agent_list)
        return f'{self._node_name}({self.id})):\n\tcapacity:{self.capacity}\n\tagents:{agents}'

    @property
    def contact_rate(self):
        poblation_rate = len(self.agent_list) / self.capacity
        if poblation_rate < 0.5:
            return 0.1
        elif poblation_rate < 0.8:
            return 0.5
        else:
            return 0.8


class BlockNode(SimNode):
    def __init__(self, capacity: int, id: Tuple, addr:Tuple[int, int]):
        """
        Class representing the block node of the simulation

        Args:
            capacity (int): Represents the max amount of people the node is designed to support.
            id (Tuple): position of the block if it where in a grid based representation.
        """
        super().__init__(capacity, id, addr)
        pass 


class Workspace(SimNode):
    def __init__(self, capacity: int, id: Hashable, addr:Tuple[int, int], opening_hours = 8, closing_hours = 16):
        """
        Class representing a workspace in the city

        Args:
            capacity (int): Represents the max amount of people the node is designed to support.
        """
        super().__init__(capacity, id, addr)
        self.opening_hours = opening_hours
        self.closing_hours = closing_hours


class PublicPlace(SimNode):
    def __init__(self, capacity: int, id: Hashable, addr:Tuple[int, int]):
        """
        Class representing a workspace in the city

        Args:
            capacity (int): Represents the max amount of people the node is designed to support.
        """
        super().__init__(capacity, id, addr)
        pass  
    
class Hospital(Workspace):
    def __init__(self, capacity: int, id: Hashable, addr:Tuple[int, int]):
        """
        Class representing a hospital in the city

        Args:
            capacity (int): Represents the max amount of people the node is designed to support.
        """
        super().__init__(capacity, id, addr)
        pass 
    
class BusStop(PublicPlace):
    def __init__(self, capacity: int, id: Hashable, addr:Tuple[int, int]):
        """
        Class representing a bus_stops in the city

        Args:
            capacity (int): Represents the max amount of people the node is designed to support.
        """
        super().__init__(capacity, id, addr)
        pass 
    
class HouseNode(SimNode):
    def __init__(self, capacity: int, id: Hashable, addr: Tuple[int], contact_rate: Callable[..., Any] = None):
        super().__init__(capacity, id, addr, contact_rate)