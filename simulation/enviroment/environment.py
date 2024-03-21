from simulation.agents import Agent
from simulation.epidemic import EpidemicModel

from typing import List, Tuple
import random
import numpy as np
from utils.graph import Node,Graph
class Building:
    def __init__(self, name: str, location: Tuple[float, float], building_type: str = None):
        """
        Initialize a building.

        Parameters:
            name (str): The name of the building.
            location (Tuple[float, float]): The location of the building as a (x, y) tuple.
        """
        self.building_type = building_type # Ejemplo: 'home', 'workplace', 'school', 'public'
        self.name = name
        self.location = location

class Environment:
    def __init__(self,num_agents: int, epidemic_model: EpidemicModel,map: Graph = None):
        """
        Initialize the environment.

        Parameters:
            num_agents (int): The number of agents to initialize in the environment.
        """
        if map:
            self.map = map
            
        self.agents: List[Agent] = []
        self.buildings: List[Building] = []
        self.epidemic_model = epidemic_model
        self.initialize_agents(num_agents)
        # self.initialize_spaces()

    def initialize_agents(self, num_agents: int):
        """
        Initialize agents within the environment.

        Parameters:
            num_agents (int): The number of agents to initialize.
        """
        infected_agents = random.randint(0, num_agents/2)
        
        
        for i in range(num_agents):
            agent = Agent(unique_id=i, status='infected') if i < infected_agents else Agent(unique_id=i)
            pos = random.randint(1, len(self.map.nodes))
            self.add_agent(agent, pos)

    def add_agent(self, agent: Agent, pos: int):
        """
        Add an agent to the environment at a specified location.

        Parameters:
            agent (Agent): The agent to add.
            x (int): The x-coordinate of the agent's location.
            y (int): The y-coordinate of the agent's location.
        """
        agent.location = pos
        self.agents.append(agent)

    def add_building(self, building: Building):
        """
        Add a building to the environment.

        Parameters:
            building (Building): The building to add.
        """
        self.buildings.append(building)

    def initialize_spaces(self):
        """
        Add spaces to the environment.
        """
        self.add_building(Building("Home", (100, 100), "home"))
        self.add_building(Building("Workplace", (200, 200), "workplace"))
        self.add_building(Building("School", (300, 300), "school"))
        self.add_building(Building("Park", (400, 400), "public"))
        self.add_building(Building("Hospital", (500, 500), "hospital"))

    def move_agent(self, agent: Agent, parameter: int):
        """
        Move an agent to a new location.

        Parameters:
            agent (Agent): The agent to move.
        """
        
        prev_location = agent.location
        
        agent.location = parameter
        
                
    def get_neighbors(self, agent: Agent, radius: int = 20) -> List[Agent]:
        """
        Get neighboring agents within a certain radius of a given agent.

        Parameters:
            agent (Agent): The agent to find neighbors for.
            radius (float): The radius within which to search for neighbors. Default is 1.0.

        Returns:
            List[Agent]: A list of neighboring agents.
        """
        neighbors = []
        
        for _agent in self.agents:
            if agent.location == _agent.location:
                neighbors.append(_agent)
        
        return neighbors

    def step(self):
        """
        Perform a simulation step, where agents take actions.
        """
        for agent in self.agents:
            # Implement agent actions for each step
            action, parameter = agent.act()
            if action ==  "move":
                self.move_agent(agent,parameter)
            pass
        self.epidemic_model.step([(agent, self.get_neighbors(agent)) for agent in self.agents])


if __name__ == '__main__':
    # Example usage
    env = Environment(x_limit=100.0, y_limit=100.0, num_agents=10)
    building1 = Building("Workplace", (50.0, 50.0))
    building2 = Building("Park", (30.0, 70.0))
    env.add_building(building1)
    env.add_building(building2)
