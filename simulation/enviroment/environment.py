from simulation.agents.agents import Agent
from simulation.agents.agent_arquitecture import BehaviorLayer
from simulation.epidemic.epidemic_model import EpidemicModel
from simulation.utils.sim_nodes import CitizenPerceptionNode as CPNode
from typing import Tuple, List
import random
from utils.graph import Graph
import logging

logger = logging.getLogger(__name__)

class Environment:
    def __init__(self,num_agents: int, epidemic_model: EpidemicModel, map: Graph):
        """
        Initialize the environment.

        Parameters:
            num_agents (int): The number of agents to initialize in the environment.
        """
        self.map = map    
        self.agents: List[Agent] = []
        self.epidemic_model = epidemic_model
        logger.debug('=== Initializing Agents ===')
        self.initialize_citizen_agents(num_agents)

    def initialize_citizen_agents(self, num_agents: int):
        """
        Initialize agents within the environment.

        Parameters:
            num_agents (int): The number of agents to initialize.
        """
        infected_agents = random.randint(0, int(num_agents/2))
        #TODO Adding the required agent components:
        # - Wi
        # - BBC
        # - PBC
        # - CC
        # - Knowlege Base
        for i in range(num_agents):
            mind_map = self.generate_citizen_mind_map()
            agents_wi  = WorldInterface(self.map, mind_map)
            agent = Agent(unique_id=i, status='infected', mind_map = mind_map, wi_component = agents_wi) if i < infected_agents else Agent(unique_id=i, mind_map = mind_map, wi_component = agents_wi)
            agents_bbc = BehaviorLayer(agent.mind_map, agent.knowledge_base)
            agent.bbc = agents_bbc
            location = random.choice(list(self.map.nodes.keys()))
            self.add_agent(agent, location)

    def add_agent(self, agent: Agent, pos: int):
        """
        Add an agent to the environment at a specified location.

        Parameters:
            agent (Agent): The agent to add.
            x (int): The x-coordinate of the agent's location.
            y (int): The y-coordinate of the agent's location.
        """
        agent.location = pos #TODO: change this so the agent position is a knolege\believe
        self.map.nodes[pos].agent_list.append(agent.unique_id)
        self.agents.append(agent)

    def generate_citizen_mind_map(self):
        mind_map = Graph()

        for node_id in self.map.nodes.keys():
            old_node = self.map.nodes[node_id]
            new_node = CPNode(old_node.id)
            mind_map.add_node(new_node)

        mind_map.edges = self.map.edges.copy()
        
        return mind_map

    def get_neighbors(self, agent: Agent):
        """
        Get the neighbors of an agent.

        Parameters:
            agent (Agent): The agent to get neighbors for.

        Returns:
            List[int]: A list of neighboring agent IDs.
        """
        agents_node = self.map.nodes[agent.location]
        return [self.agents[agent_id] for agent_id in agents_node.agent_list if agent_id != agent.unique_id]

    def step(self):
        """
        Perform a simulation step, where agents take actions.
        """
        for agent in random.sample(self.agents, len(self.agents)):
            agent.step()
        self.epidemic_model.step([(agent, self.get_neighbors(agent), self.map.nodes[agent.location].contact_rate) for agent in self.agents])
        pass


class WorldInterface:
    def __init__(self, map: Graph, agent_mind_map: Graph) -> None:
        self.map = map
        self.agent_mind_map = agent_mind_map

    def act(self, agent: Agent, action: str, parameters: list):
        if action == 'move':
            logger.debug(f'Agent {agent.unique_id} is moving to {parameters[0]}')
            self.move_agent(agent, *parameters)
        else:
            logger.error(f'Action {action} not recognized')

    def comunicate(self, emiter, reciever, message):
        raise NotImplementedError

    def recieve_comunication(self, agent, message):
        raise NotImplementedError

    def percieve(self, agent: Agent):
        def density_classifier(node_population, node_capacity):
            node_density = node_population/node_capacity
            if node_density < 0.5:
                return 'low'
            elif node_density < 0.8:
                return 'medium'
            elif node_density <= 1.0:
                return 'high'
            else:
                return 'very_high'
        
        new_perception = {}

        current_node = self.map.nodes[agent.location]
        current_node_perception = CPNode(current_node.id, density_classifier(len(current_node.agent_list), current_node.capacity))
        new_perception[current_node.id] = current_node_perception

        for neighbor_key in self.map.get_neighbors(agent.location):
            neighbor_node = self.map.nodes[neighbor_key]
            node_density = density_classifier(len(neighbor_node.agent_list), neighbor_node.capacity)
            new_perception[neighbor_key] = CPNode(neighbor_key, node_density)

        return new_perception

    def move_agent(self, agent: Agent, pos: int):
        """
        Move an agent to a new location.

        Parameters:
            agent (Agent): The agent to move.
        """
        pos = tuple(pos)
        # Getting the previous location
        prev_location = agent.location

        # Getting the current location neighbors
        prev_neighbors = self.map.get_neighbors(prev_location)

        # Checking if the new location is a neighbor of the previous location
        if pos not in prev_neighbors:
            logger.error(f'Agent {agent.unique_id} cannot move to {pos} from {prev_location}')
            return
        
        # Removing the agent from the previous location
        self.map.nodes[prev_location].agent_list.remove(agent.unique_id)

        # Adding the agent to the new location
        agent.location = pos
        self.map.nodes[pos].agent_list.append(agent.unique_id) 