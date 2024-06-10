from simulation.agents.agents import Agent, Canelo
from simulation.agents.agent_arquitecture import BehaviorLayer, LocalPlanningLayer, CooperativeLayer, Knowledge, KnowledgeCanelo
from simulation.epidemic.epidemic_model import EpidemicModel
from simulation.enviroment.sim_nodes import CitizenPerceptionNode as CPNode
from simulation.enviroment.sim_nodes import BlockNode, Hospital, HouseNode, PublicPlace, BusStop, Workspace
from simulation.enviroment.map import Terrain
from ai.search import a_star, bfs, AgentPathProblem, astar_search, path_states
from typing import Tuple, List
import random
from simulation.enviroment.graph import Graph
import logging
from pyswip import Prolog

logger = logging.getLogger(__name__)

class Environment:
    """
    Class representing the simulation environment.

    Attributes:
        map (Terrain): The terrain of the simulation.
        agents (List[Agent]): The list of agents in the environment.
        epidemic_model (EpidemicModel): The epidemic model for the simulation.
    """
    def __init__(self, num_agents: int, epidemic_model: EpidemicModel, map: Terrain, solution:list =None ):
        """
        Initialize the environment.

        Args:
            num_agents (int): The number of agents to initialize in the environment.
            epidemic_model (EpidemicModel): The epidemic model for the simulation.
            map (Terrain): The terrain of the simulation.
        """
        self.map: Terrain = map    
        self.agents: List[Agent] = []
        self.dead_agents: set[Agent] = set()
        self.canelo = None
        self.epidemic_model = epidemic_model
        self.dissease_step_progression = []
        logger.debug('=== Initializing Agents ===')
        self.solution = solution
        self.initialize_citizen_agents(num_agents)
        self.initialize_canelo_agent()
        self.initialize_relations()
        self.hospitals_with_patients = []

        def kill_agent(agent):
            self.dead_agents.add(agent.unique_id)
            agent_location = agent.location
            self.map[agent_location].agent_list.remove(agent.unique_id)
            # agent.knowledge_base = None

        self.epidemic_model.kill_agent = kill_agent

    def initialize_citizen_agents(self, num_agents: int) -> None:
        """
        Initialize agents within the environment.

        Args:
            num_agents (int): The number of agents to initialize.
        """
        # infected_agents = random.randint(1, int(num_agents/2))
        infected_agents = int(num_agents/2)

        for i in range(num_agents):
            mind_map = self.generate_citizen_mind_map()
            kb = self._initialize_agents_knowledge(i)

            agents_wi  = WorldInterface(self, self.map, mind_map, kb)
            agents_bbc = BehaviorLayer(agents_wi, kb, mind_map)
            agents_pbc = LocalPlanningLayer(agents_bbc, kb, mind_map)
            agent_cc = CooperativeLayer(agents_pbc, kb, mind_map)

            agent = Agent(
                unique_id=i, 
                mind_map=mind_map,
                lp_component=agents_pbc,
                bb_component=agents_bbc,
                c_component=agent_cc,
                wi_component=agents_wi,
                knowledge_base=kb
                )
            
            if i < infected_agents:
                self.epidemic_model._infect_citizen(agent)

            location = random.choice(list(self.map.keys()))
            self.add_agent(agent, location)

    def _initialize_agents_knowledge(self, id):
        kb = Knowledge()
        house = random.choice(self.map.houses)
        house.add_person(id)
        kb.add_home(house.id)
        is_medic = random.choice([True, False])
        
        if is_medic:  
            work = random.choice(self.map.hospitals)
            work.add_person(id)
            kb.add_work_place(self.map[work.id])
            kb.add_is_medical_personnel(True)
        else:
            work = random.choice(self.map.works)
            work.add_person(id)
            kb.add_work_place(self.map[work.id])
            kb.add_is_medical_personnel(False)
        #TODO: Keep Initializing the KB
        
        return kb
    
    def create_family(self, home):
        if len(home.persons) <= 1:
            return []
        id_list = [agent_id for agent_id in home.persons]
        for agent_id in home.persons:
            agent = self.agents[agent_id]
            friends_list = id_list.copy()
            if agent_id in friends_list:
                friends_list.remove(agent_id)
            agent.knowledge_base.add_friends(friends_list)

    def create_work_relations(self, work):
        if len(work.persons) <= 1:
            return []
        id_list = [agent_id for agent_id in work.persons]
        for agent_id in work.persons:
            friends_amount = random.randint(1, int(len(work.persons)/2))
            posible_friends = random.sample(id_list, friends_amount)
            agent = self.agents[agent_id]
            if agent_id in posible_friends:
                friends_list = posible_friends.remove(agent_id)
            else:
                friends_list = posible_friends
                if friends_list:
                    agent.knowledge_base.add_friends(friends_list)

    def initialize_relations(self):
        terrain = self.map
        houses = terrain.houses
        work_places = terrain.works

        for house in houses:
            self.create_family(house)

        for work_place in work_places:
            self.create_work_relations(work_place)

    def initialize_canelo_agent(self):
        kb = KnowledgeCanelo()
        mind_map = self.generate_citizen_mind_map()
        
        agents_wi  = WorldInterfaceCanelo(self.map, self.agents, kb, self)
        agents_bbc = BehaviorLayer(agents_wi, kb, mind_map)
        agents_pbc = LocalPlanningLayer(agents_bbc, kb, mind_map)
        agent_cc = CooperativeLayer(agents_pbc, kb, mind_map)
        
        agent = Canelo( 
                mind_map=mind_map, 
                bb_component=agents_bbc,
                lp_component=agents_pbc,
                c_component=agent_cc,
                wi_component=agents_wi,
                knowledge_base=kb,
                solution = self.solution
                )
        
        self.canelo = agent
        
    def add_agent(self, agent: Agent, pos: int) -> None:
        """
        Add an agent to the environment at a specified location.

        Args:
            agent (Agent): The agent to add.
            pos (int): The position of the agent's location.
        """
        agent.location = pos
        agent.knowledge_base.add_current_location(pos)
        self.map[pos].agent_list.append(agent.unique_id)
        self.agents.append(agent)

    def generate_citizen_mind_map(self) -> Graph:
        """
        Generate a mind map for a citizen agent.

        Returns:
            Graph: The generated mind map.
        """
        mind_map = Graph()
        for node_id in self.map.keys():
            old_node = self.map[node_id]
            if isinstance(old_node, BlockNode):
                node_type = 'block'
            elif isinstance(old_node, Hospital):
                node_type = 'hospital'
            elif isinstance(old_node, Workspace):
                node_type = 'work_space'
            elif isinstance(old_node, BusStop):
                node_type = 'bus_stop'
            elif isinstance(old_node, PublicPlace):
                node_type = 'public_space'
            elif isinstance(old_node, HouseNode):
                node_type = 'house'
            else:
                raise ValueError(f'node of type unknown{type(old_node)}')
            
            new_node = CPNode(old_node.addr, old_node.id, node_type)
            if node_type in ['hospital', 'work_space', 'bus_stop', 'public_space']:
                new_node.oppening_hours = old_node.opening_hours
                new_node.closing_hours = old_node.closing_hours
                new_node.is_open = old_node.is_open
            mind_map.add_node(new_node)

        mind_map.edges = self.map.graph.edges.copy()
        
        return mind_map

    def get_neighbors(self, agent: Agent) -> List[Agent]:
        """
        Get the neighbors of an agent.

        Args:
            agent (Agent): The agent to get neighbors for.

        Returns:
            List[Agent]: A list of neighboring agents.
        """
        agents_node = self.map.nodes[agent.location]
        return [self.agents[agent_id] for agent_id in agents_node.agent_list if agent_id != agent.unique_id]

    def step(self, step_num: int) -> None:
        """
        Perform a simulation step, where agents take actions.

        Args:
            step_num (int): The current step number of the simulation.
        """
        for i, hospital in enumerate(self.hospitals_with_patients.copy()):
            hospital.attend_patient(self.canelo)
            if len(hospital.patients) == 0:
                self.hospitals_with_patients.pop(i)
                
        for agent in random.sample(self.agents, len(self.agents)):
            if agent.unique_id in self.dead_agents:
                continue
            logger.info(f'Step of agent {agent.unique_id}')
            agent.step(step_num)
            self._debug_agent_k(agent.knowledge_base)
        
        infected_agents = self._count_infected_agents()
        self.canelo.step(infected_agents)
        
        ocupied_nodes = [([self.agents[agent_id] for agent_id in node.agent_list], node.contact_rate) for node in self.map.graph.nodes.values() if node.agent_list]
        self.epidemic_model.step(ocupied_nodes)

        self.dissease_step_progression.append(self.get_dissease_stats())

    def _debug_agent_k(self, agent_k:Knowledge):
        logger.debug(f'Knowlege Base Facts:')
        for fact in agent_k.facts.keys():
            logger.debug(f'{fact}:')
            logger.debug(f'{agent_k[fact]}')

    def _count_infected_agents(self):
        infected = 0
        for agent in self.agents:
            if agent.status == 'symptomatic':
                infected += 1
            if agent.status == 'critical':
                infected += 2
            if agent.status == 'terminal':
                infected += 3
    
        return infected
    
    def _log_fact_type(self, fact_type, facts):
        logger.debug(f'All {fact_type} facts:')
        for fact in facts:
            for key in fact.keys():
                logger.debug(f'{key}: {fact[key]}')
        pass

    def get_dissease_stats(self):
        agent_dist = {
            'susceptible': 0,
            'asymptomatic': 0,
            'symptomatic': 0,
            'critical': 0,
            'terminal': 0,
            'dead': 0,
            'recovered': 0
        }
        for agent in self.agents:
            agent_dist[agent.status] += 1

        return agent_dist

class WorldInterface:
    """
    Class representing the world interface for an agent.

    Attributes:
        map (Graph): The map of the simulation.
        agent_mind_map (Graph): The mind map of the agent.
        agent_kb (Knowledge): The knowledge base of the agent.
    """
    def __init__(self, enviroment: Environment, map: Graph, agent_mind_map: Graph, knowledge_base: Knowledge) -> None:
        self.enviroment = enviroment
        self.map = map
        self.agent_mind_map = agent_mind_map
        self.agent_kb = knowledge_base

    def act(self, agent: Agent, action: str, parameters: list = None) -> None:
        """
        Perform an action for an agent.

        Args:
            agent (Agent): The agent performing the action.
            action (str): The action to perform.
            parameters (list): The parameters for the action.
        """
        if isinstance(parameters, int):
            parametersList = []
            parametersList.append(parameters)
            parameters = parametersList
        
        if action == 'move':#TODO: Change to a heuristic to another when needed
            logger.info(f'Agent {agent.unique_id} is moving to {parameters[0]} from {agent.location}')
            # a = a_star(self.map, agent.location, parameters[0])
            if agent._last_path and agent._last_path[-1] == parameters[0]:
                path = agent._last_path
            else:
                map = self.agent_mind_map
                if parameters[1]:
                    problem = AgentPathProblem(map[agent.location], map[parameters[0]], map, 'minimum_contact_path')          
                else:
                    problem = AgentPathProblem(map[agent.location], map[parameters[0]], map)
                path = path_states(astar_search(problem))[1:]#TODO: change g in a_star for min_exposure
                agent._last_path = path

            if agent._last_path:
                self.move_agent(agent, agent._last_path.pop(0))
            pass
   
        elif action == 'wear_mask':
            logger.info(f'Agent {agent.unique_id} is using mask')
            agent.masked = True 
            
        elif action == 'remove_mask':
            logger.info(f'Agent {agent.unique_id} is removing mask')
            agent.masked = False 
        
        elif action == 'get_vaccinated':
            hospital = self.map[parameters[0]]
            hospital.add_patient_consult(agent)
            if hospital not in self.enviroment.hospitals_with_patients:
                self.enviroment.hospitals_with_patients.append(hospital)
            
        elif action == 'nothing':
            logger.info(f'Agent {agent.unique_id} is doing nothing')

        elif action == 'send_message':
            logger.info(f'Agent {agent.unique_id} is sending to agent {parameters[1]} the following message:\n\t{parameters[0]} ')
            self.comunicate(agent.unique_id, parameters[0], parameters[1])
        
        elif action == 'work':
            logger.info(f'Agent {agent.unique_id} is working')
        
        elif not action:            
            logger.info(f'Agent {agent.unique_id} action is empty')

    def percieve(self, agent: Agent, step_num: int) -> dict:
        """
        Perceive the environment around an agent.

        Args:
            agent (Agent): The agent perceiving the environment.
            step_num (int): The current step number of the simulation.

        Returns:
            dict: A dictionary of perceived environments.
        """
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
        if isinstance(current_node, BlockNode):
            node_type = 'block'
        elif isinstance(current_node, Hospital):
            node_type = 'hospital'
        elif isinstance(current_node, Workspace):
            node_type = 'work_space'
        elif isinstance(current_node, BusStop):
            node_type = 'bus_stop'
        elif isinstance(current_node, PublicPlace):
            node_type = 'public_space'
        elif isinstance(current_node, HouseNode):
            node_type = 'house'
        else:
            raise ValueError(f'node of type unknown{type(current_node)}')
        current_node_perception = CPNode(current_node.addr, current_node.id, node_type, density_classifier(len(current_node.agent_list), current_node.capacity))
        new_perception[current_node.addr] = current_node_perception
        if node_type in ['hospital', 'works_space', 'bus_stop', 'public_space']:
            current_node_perception.oppening_hours = current_node.opening_hours
            current_node_perception.closing_hours = current_node.closing_hours
            current_node_perception.is_open = current_node.is_open
        current_node_perception.mask_required = current_node.mask_required


        return new_perception

    def move_agent(self, agent: Agent, pos: int) -> None:
        """
        Move an agent to a new location.

        Args:
            agent (Agent): The agent to move.
            pos (int): The new location for the agent.
        """
        prev_location = agent.location

        prev_neighbors = self.map.graph.get_neighbors(prev_location)

        if pos not in prev_neighbors:
            logger.error(f'Agent {agent.unique_id} cannot move to {pos} from {prev_location}')
            return
        
        self.map.graph.nodes[prev_location].agent_list.remove(agent.unique_id)

        agent.location = pos
        logger.info(f'Agent moved to {pos}')
        self.map.graph.nodes[pos].agent_list.append(agent.unique_id)
    
    def comunicate(self, sender: Agent, message: str, reciever_id: int) -> None:
        """
        Communicate a message from one agent to another.
        
        Args:
            emiter (Agent): The agent sending the message.
            reciever (Agent): The agent receiving the message.
            message (str): The message to send.
        """
        pass

class WorldInterfaceCanelo:
    """
    Class representing the world interface for canelo.

    Attributes:
        map (Graph): The map of the simulation.
        agent_mind_map (Graph): The mind map of the agent.
        agent_kb (Knowledge): The knowledge base of the agent.
    """
    def __init__(self, map: Terrain, list_agents:list[Agent], knowledge_base: KnowledgeCanelo, enviroment: Environment) -> None:
        self.map = map
        self.list_agents = list_agents
        self.agent_kb = knowledge_base
        self.env = enviroment

    def act(self, agent: Canelo, action: str) -> None:
        """
        Perform an action for an agent.

        Args:
            agent (Agent): The agent performing the action.
            action (str): The action to perform.
            parameters (list): The parameters for the action.
        """
        
        if action == 'temporary_closure_pp':
            logger.info(f'Canelo is transmitting temporaly closure in public places')
            for node in self.map.graph.nodes.values():
                if isinstance(node, PublicPlace):
                    node.is_open = False
                else:
                    continue
            
            for agent in self.list_agents:
                for node in self.map.graph.nodes.values():
                    if isinstance(node, PublicPlace):
                        self.comunicate( agent, action,node)
        
        elif action == 'temporary_closure_work':
            logger.info(f'Canelo is transmitting temporaly closure in work')
            for node in self.map.graph.nodes.values():
                if isinstance(node, Workspace) and not isinstance(node, Hospital):
                    node.is_open = False
                else:
                    continue
            
            for agent in self.list_agents:
                for node in self.map.graph.nodes.values():
                    if isinstance(node, Workspace) and not isinstance(node, Hospital):
                        self.comunicate( agent, action,node)
        
        elif action == 'mask_use':
            logger.info(f'Canelo is transmitting use mask')
            for agent in self.list_agents:
                self.comunicate( agent, action)
            
            for node in self.map.graph.nodes.values():
                if isinstance(node, HouseNode):
                    continue
                node.mask_required = True
        
        elif action == 'remove_mask':
            logger.info(f'Canelo is transmitting not use mask')
            for agent in self.list_agents:
                self.comunicate( agent, action)
            
            for node in self.map.graph.nodes.values():
                if isinstance(node, HouseNode):
                    continue
                node.mask_required = False
        
        elif action == 'quarantine':
            logger.info(f'Canelo is transmitting go quarantine')
            for agent in self.list_agents:
                self.comunicate( agent, action)
        
        elif action == 'social_distancing':
            logger.info(f'Canelo is transmitting social_distancing')
            for agent in self.list_agents:
                self.comunicate( agent, action)     
        
        elif action == 'tests_and_diagnosis':
            logger.info(f'Canelo is transmitting tests_and_diagnosis')
            for agent in self.list_agents:
                self.comunicate( agent, action)
        
        elif action == 'contact_tracing':
            logger.info(f'Canelo is transmitting contact_tracing')
            for agent in self.list_agents:
                self.comunicate( agent, action)

        elif action == 'vaccination':
            logger.info(f'Canelo is transmitting vaccination')
            for agent in self.list_agents:
                self.comunicate( agent, action)
        
        elif action == 'nothing':
            try:
                logger.info(f'Agent {agent.unique_id} is doing nothing')
            except:
                logger.info(f'Agent canelo is doing nothing')

        else:
            logger.error(f'Action {action} not recognized')

    def comunicate(self, reciever: Agent, message, node = None) -> None:
        """
        Communicate a message from one agent to another.

        Args:
            emiter (Agent): The agent sending the message.
            reciever (Agent): The agent receiving the message.
            message (str): The message to send.
        """
        Id = None
        if node:
            Id = node.id
            
        if message == 'temporary_closure_pp':
            message1 = {
                'info': 'is_open' , 
                'value': False,
                'location': Id
            }
            reciever.recieve_message( -1, message1, 'map')
        
        elif message == 'temporary_closure_work': 
            message1 = {
                'info': 'is_open' , 
                'value': False,
                'location': Id
            }
            reciever.recieve_message( -1, message1, 'map')
        
        if message == 'mask_use':
            message1 = {
                'info': 'mask_necessity' , 
                'value': True
            }
            reciever.recieve_message(-1, message1, 'measure')
            
            
        elif message == 'remove_mask':
            message1 = {
                'info': 'mask_necessity' , 
                'value': False
            }
            reciever.recieve_message(-1, message1, 'measure')
        
        elif message == 'quarantine':
            message1 = {
                'info': 'quarantine_necessity' , 
                'value': True
            }
            reciever.recieve_message(-1, message1, 'measure')
              
        elif message == 'tests_and_diagnosis':
            message1 = {
                'info': 'tests_and_diagnosis_necessity' , 
                'value': True
            }
            reciever.recieve_message(-1, message1, 'measure')
        
        elif message == 'social_distancing':
            message1 = {
                'info': 'social_distancing' , 
                'value': True
            }
            reciever.recieve_message(-1, message1, 'measure')

        elif message == 'vaccination':
            message1 = {
                'info': 'vaccination_necessity' , 
                'value': True
            }
            reciever.recieve_message(-1, message1, 'measure')

    def percieve(self, agent: Agent, step_num: int) -> dict:
        """
        Perceive the environment around an agent.

        Args:
            agent (Agent): The agent perceiving the environment.
            step_num (int): The current step number of the simulation.

        Returns:
            dict: A dictionary of perceived environments.
        """
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
        if isinstance(current_node, BlockNode):
            node_type = 'block'
        elif isinstance(current_node, Hospital):
            node_type = 'hospital'
        elif isinstance(current_node, Workspace):
            node_type = 'work_space'
        elif isinstance(current_node, BusStop):
            node_type = 'bus_stop'
        elif isinstance(current_node, PublicPlace):
            node_type = 'public_space'
        elif isinstance(current_node, HouseNode):
            node_type = 'house'
        else:
            raise ValueError(f'node of type unknown{type(current_node)}')
        current_node_perception = CPNode(current_node.addr, current_node.id, node_type, density_classifier(len(current_node.agent_list), current_node.capacity))
        if node_type in ['hospital', 'works_space', 'bus_stop', 'public_space']:
            current_node_perception.oppening_hours = current_node.opening_hours
            current_node_perception.closing_hours = current_node.closing_hours
            current_node_perception.is_open = current_node.is_open

        new_perception[current_node.addr] = current_node_perception



        return new_perception
