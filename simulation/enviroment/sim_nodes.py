from utils.graph import Node
from typing import Hashable, Tuple

class PerceptionNode(Node):
    def __init__(self, id: Hashable = None) -> None:
        super().__init__(id)
        self._node_name = "PerceptionNode"

class CitizenPerceptionNode(PerceptionNode):
    def __init__(self, id: Hashable, capacity_status: str = 'unknown', information_source: str = 'perception') -> None:
        super().__init__(id)
        self.capacity_status = capacity_status
        self.information_source = information_source


class SimNode(Node):
    def __init__(self, capacity: int, id: Hashable):
        """
        Class representing the base node of the simulation

        Args:
            capacity (int): Represents the capacity of the node.
            id (int): The identifier of the node.
        """
        super().__init__(id)
        self.capacity = capacity
        self.agent_list = []
        self.transmition_modifier = 1
        self.contact_rate = 0

    def __str__(self):
        agents = '\n\t'.join(self.agent_list)
        return f'{self._node_name}({self.id})):\n\tcapacity:{self.capacity}\n\tagents:{agents}'


class BlockNode(SimNode):
    def __init__(self, capacity: int, id: Tuple):
        """
        Class representing the block node of the simulation

        Args:
            capacity (int): Represents the max amount of people the node is designed to support.
            id (Tuple): position of the block if it where in a grid based representation.
        """
        super().__init__(capacity, id)
        pass 


class Workspace(SimNode):
    def __init__(self, capacity: int, id: Hashable):
        """
        Class representing a workspace in the city

        Args:
            capacity (int): Represents the max amount of people the node is designed to support.
        """
        super().__init__(capacity, id)
        pass    


class PublicPlace(SimNode):
    def __init__(self, capacity: int, id: Hashable):
        """
        Class representing a workspace in the city

        Args:
            capacity (int): Represents the max amount of people the node is designed to support.
        """
        super().__init__(capacity, id)
        pass  