from simulation.enviroment.graph import Node
from typing import Hashable, Tuple, Callable, Any

class PerceptionNode(Node):
    """
    Class representing a perception node in the simulation.

    Args:
        addr (Tuple[int, int]): The address of the node.
        id (Hashable, optional): The identifier of the node. Defaults to None.
    """
    def __init__(self, addr: Tuple[int, int], id: Hashable = None) -> None:
        super().__init__(id)
        self._node_name = "PerceptionNode"
        self.addr = addr

class CitizenPerceptionNode(PerceptionNode):
    """
    Class representing a citizen perception node in the simulation.

    Args:
        addr (Tuple[int, int]): The address of the node.
        id (Hashable): The identifier of the node.
        capacity_status (str, optional): The status of the node's capacity. Defaults to 'unknown'.
        information_source (str, optional): The source of information for the node. Defaults to 'perception'.
    """
    def __init__(self, addr:Tuple[int, int], id: Hashable, node_type:str, capacity_status: str = 'unknown', information_source: str = 'perception') -> None:
        super().__init__(addr, id)
        self.capacity_status = capacity_status
        self.information_source = information_source
        self.node_type = node_type

class SimNode(Node):
    """
    Class representing the base node of the simulation.

    Args:
        capacity (int): Represents the capacity of the node.
        id (Hashable): The identifier of the node.
        addr (Tuple[int, int]): The address of the node.
        contact_rate (Callable, optional): The contact rate of the node. Defaults to None.
    """
    def __init__(self, capacity: int, id: Hashable, addr: Tuple[int, int], contact_rate: Callable = None):
        super().__init__(id)
        self.capacity = capacity
        self.agent_list = []
        self.addr = addr

    def __str__(self):
        agents = '\n\t'.join(str(self.agent_list))
        return f'{self._node_name}({self.id})):\n\tcapacity:{self.capacity}\n\tagents:{agents}'

    @property
    def contact_rate(self):
        """
        Calculates the contact rate based on the population rate.

        Returns:
            float: The contact rate of the node.
        """
        poblation_rate = len(self.agent_list) / self.capacity
        if poblation_rate < 0.5:
            return 0.1
        elif poblation_rate < 0.8:
            return 0.5
        else:
            return 0.8

class BlockNode(SimNode):
    """
    Class representing a block node in the simulation.

    Args:
        capacity (int): Represents the maximum number of people the node is designed to support.
        id (Tuple): The position of the block in a grid-based representation.
        addr (Tuple[int, int]): The address of the node.
    """
    def __init__(self, capacity: int, id: Tuple, addr: Tuple[int, int]):
        super().__init__(capacity, id, addr)

class Workspace(SimNode):
    """
    Class representing a workspace in the simulation.

    Args:
        capacity (int): Represents the maximum number of people the node is designed to support.
        id (Hashable): The identifier of the node.
        addr (Tuple[int, int]): The address of the node.
        opening_hours (int, optional): The opening hours of the workspace. Defaults to 8.
        closing_hours (int, optional): The closing hours of the workspace. Defaults to 16.
    """
    def __init__(self, capacity: int, id: Hashable, addr: Tuple[int, int], opening_hours = 8, closing_hours = 16):
        super().__init__(capacity, id, addr)
        self.opening_hours = opening_hours
        self.closing_hours = closing_hours
        self.is_open = True

class PublicPlace(SimNode):
    """
    Class representing a public place in the simulation.

    Args:
        capacity (int): Represents the maximum number of people the node is designed to support.
        id (Hashable): The identifier of the node.
        addr (Tuple[int, int]): The address of the node.
    """
    def __init__(self, capacity: int, id: Hashable, addr: Tuple[int, int], opening_hours = 8, closing_hours = 16):
        super().__init__(capacity, id, addr)
        self.opening_hours = opening_hours
        self.closing_hours = closing_hours
        self.is_open = True

class Hospital(Workspace):
    """
    Class representing a hospital in the simulation.

    Args:
        capacity (int): Represents the maximum number of people the node is designed to support.
        id (Hashable): The identifier of the node.
        addr (Tuple[int, int]): The address of the node.
    """
    def __init__(self, capacity: int, id: Hashable, addr: Tuple[int, int]):
        super().__init__(capacity, id, addr)

class BusStop(PublicPlace):
    """
    Class representing a bus stop in the simulation.

    Args:
        capacity (int): Represents the maximum number of people the node is designed to support.
        id (Hashable): The identifier of the node.
        addr (Tuple[int, int]): The address of the node.
    """
    def __init__(self, capacity: int, id: Hashable, addr: Tuple[int, int]):
        super().__init__(capacity, id, addr)

class HouseNode(SimNode):
    """
    Class representing a house node in the simulation.

    Args:
        capacity (int): Represents the maximum number of people the node is designed to support.
        id (Hashable): The identifier of the node.
        addr (Tuple[int, int]): The address of the node.
        contact_rate (Callable, optional): The contact rate of the node. Defaults to None.
    """
    def __init__(self, capacity: int, id: Hashable, addr: Tuple[int, int], contact_rate: Callable[..., Any] = None):
        super().__init__(capacity, id, addr, contact_rate)
        self.persons: list = []
        
    def add_person(self, id):
        self.persons.append(id)

    def remove_person(self, id):
        self.persons.remove(id)
