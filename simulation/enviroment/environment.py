from simulation.agents.agents import Agent
from simulation.agents.agent_arquitecture import BehaviorLayer, LocalPlanningLayer, Knowledge
from simulation.epidemic.epidemic_model import EpidemicModel
from simulation.utils.sim_nodes import CitizenPerceptionNode as CPNode
from simulation.enviroment.map import Terrain
from typing import Tuple, List
import random
from utils.graph import Graph
import logging

logger = logging.getLogger(__name__)

class Environment:
    def __init__(self,num_agents: int, epidemic_model: EpidemicModel, map: Terrain):
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
        # - CC
        for i in range(num_agents):
            mind_map = self.generate_citizen_mind_map()
            
            kb = Knowledge()
            
            house_id = random.choice(self.map.houses)
            
            kb.add_home(house_id)
            is_medic = random.choice([True, False])
            if is_medic:
                work_id = random.choice(self.map.hospitals)
                kb.add_work_place(work_id)
                kb.add_is_medical_personnel(True)
            else:
                work_id = random.choice(self.map.works)
                kb.add_work_place(work_id)
                kb.add_is_medical_personnel(True)
            
            agents_wi  = WorldInterface(self.map, mind_map, kb)
            agents_bbc = BehaviorLayer(mind_map, kb)
            agents_pbc = LocalPlanningLayer(mind_map, kb)
            
            agent = Agent(
                unique_id=i, 
                mind_map=mind_map, 
                wi_component=agents_wi,
                bb_component=agents_bbc,
                lp_component=agents_pbc,
                knowledge_base=kb
                )
            
            if i < infected_agents:
                self.epidemic_model._infect_citizen(agent)

            location = random.choice(list(self.map.keys()))
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
        self.map[pos].agent_list.append(agent.unique_id)
        self.agents.append(agent)

    def generate_citizen_mind_map(self):
        mind_map = Graph()
        for node_id in self.map.keys():
            old_node = self.map[node_id]
            new_node = CPNode(old_node.addr, old_node.id)
            mind_map.add_node(new_node)

        mind_map.edges = self.map.graph.edges.copy()
        
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

    def step(self, step_num):
        """
        Perform a simulation step, where agents take actions.
        """
        for agent in random.sample(self.agents, len(self.agents)):
            agent.step(step_num)
        # self.epidemic_model.step([([self.agents[agent_id] for agent_id in node.agent_list], node.contact_rate) for node in self.map.graph.nodes.values() if node.agent_list])


class WorldInterface:
    def __init__(self, map: Graph, agent_mind_map: Graph, knowledge_base: Knowledge) -> None:
        self.map = map
        self.agent_mind_map = agent_mind_map
        self.agent_kb = knowledge_base

    def act(self, agent: Agent, action: str, parameters: list):
        if action == 'move':
            logger.debug(f'Agent {agent.unique_id} is moving to {parameters[0]}')
            self.move_agent(agent, parameters)
        else:
            logger.error(f'Action {action} not recognized')

    def comunicate(self, emiter, reciever, message):
        raise NotImplementedError

    def recieve_comunication(self, agent, message):
        raise NotImplementedError

    def percieve(self, agent: Agent, step_num):
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

        current_node = self.map[agent.location]
        current_node_perception = CPNode(current_node.addr, current_node.id, density_classifier(len(current_node.agent_list), current_node.capacity))
        new_perception[current_node.addr] = current_node_perception

        for neighbor_key in self.map.graph.get_neighbors(agent.location):
            neighbor_node = self.map[neighbor_key]
            node_density = density_classifier(len(neighbor_node.agent_list), neighbor_node.capacity)
            new_perception[neighbor_node.addr] = CPNode(neighbor_node.addr, neighbor_key, node_density)

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