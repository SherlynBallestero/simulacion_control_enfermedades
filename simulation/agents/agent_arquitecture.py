from pyswip import Prolog
from typing import Tuple
import random
class Knowledge:
    """
    Class representing the knowledge base of an agent.

    Attributes:
        prolog (Prolog): The Prolog engine for querying the knowledge base.
    """
    def __init__(self):
        """
        Initialize the knowledge base.
        """
        self.prolog = Prolog()
        self.prolog.consult('./simulation/agents/hierarchical_agent_KB.pl')

    def add_node_k(self, node):
        list(self.prolog.query(f'add_map_node({node.id}, {node.addr}, {node.capacity_status}, {node.node_type})'))
        if node.node_type in ['hospital', 'works_space', 'bus_stop', 'public_space']:
            list(self.prolog.query(f'add_map_node({node.id}, {node.oppening_hours}, {node.closing_hours}'))
        
    def add_date_k(self, date):
        """
        Add a date to the knowledge base.

        Args:
            date (tuple): The date to add.
        """
        list(self.prolog.query(f'add_date({date[0]},{date[1]},{date[2]},{date[3]})'))
        
    def add_symptom_k(self, symptom):
        """
        Add a symptom to the knowledge base.

        Args:
            symptom (str): The symptom to add.
        """
        list(self.prolog.query(f'add_symptom({symptom})'))
    
    def add_hospital_k(self, hospital_id: int, hospital_addr: Tuple[int,int]):
        """
        Add a hospital to the knowledge base.

        Args:
            hospital_id (int): The identifier of the hospital.
            hospital_addr (str): The address of the hospital.
        """
        list(self.prolog.query(f'add_hospital({hospital_id}, {hospital_addr})'))
        
    def add_home(self, home_id: int):
        """
        Add a home to the knowledge base.

        Args:
            home_id (int): The identifier of the home.
        """
        list(self.prolog.query(f'add_home({home_id})'))
    
    def add_work_place(self, wp_id: int):
        """
        Add a workplace to the knowledge base.

        Args:
            wp_id (int): The identifier of the workplace.
        """
        list(self.prolog.query(f'add_work_place({wp_id})'))
    
    def add_open_place(self, id: int, open: bool):
        """
        Add an open place to the knowledge base.

        Args:
            id (int): The identifier of the place.
            open (bool): Whether the place is open.
        """
        list(self.prolog.query(f'add_open_place({id}, {str(open).lower()})'))
    
    def add_open_hours(self, id: int, opening_hours: int, closing_hours: int):
        """
        Add open hours to the knowledge base.

        Args:
            id (int): The identifier of the place.
            opening_hours (int): The opening hours of the place.
            closing_hours (int): The closing hours of the place.
        """
        list(self.prolog.query(f'add_open_hours_place({id}, {opening_hours}, {closing_hours})'))
    
    def add_dissease_symptoms(self, symptom_list: list):
        """
        Add disease symptoms to the knowledge base.

        Args:
            symptom_list (list): The list of symptoms.
        """
        list(self.prolog.query(f'add_dissease_symptoms({symptom_list})'))
    
    def add_is_medical_personnel(self, medical_personnel: bool):
        """
        Add medical personnel information to the knowledge base.

        Args:
            medical_personnel (bool): Whether the agent is medical personnel.
        """
        list(self.prolog.query(f'add_if_is_medical_personal({str(medical_personnel).lower()})'))
    
    def add_mask_necessity(self, mask_necessity: bool):
        """
        Add mask necessity information to the knowledge base.

        Args:
            mask_necessity (bool): Whether a mask is necessary.
        """
        list(self.prolog.query(f'add_mask_necessity({mask_necessity})'))
    
    def add_mask_requirement(self, place_id: int, requirement: bool):
        """
        Add mask requirement information to the knowledge base.

        Args:
            place_id (int): The identifier of the place.
            requirement (bool): Whether a mask is required.
        """
        list(self.prolog.query(f'add_place_to_use_mask({place_id}, {requirement})'))
    
    def query(self, queryString):
        """
        Query the knowledge base.

        Args:
            queryString (str): The query string.

        Returns:
            list: The results of the query.
        """
        return list(self.prolog.query(queryString))
        
class BehaviorLayer:
    """
    Class representing the behavior layer of an agent.

    Attributes:
        world_model (Graph): The world model of the agent.
        knowledge (Knowledge): The knowledge base of the agent.
    """
    def __init__(self, world_model, knowledge: Knowledge):
        """
        Initialize the behavior layer.

        Args:
            world_model (Graph): The world model of the agent.
            knowledge (Knowledge): The knowledge base of the agent.
        """
        self.world_model = world_model
        self.knowledge = knowledge
        self.add_map_to_k()

    def add_map_to_k(self):
        """
        Add the world model to the knowledge base.
        """
        k = self.knowledge
        for node in self.world_model.nodes.values():
            if node.node_type == 'hospital':
                k.add_node_k(node)
            elif node.node_type == 'block':
                k.add_node_k(node)
            elif node.node_type == 'public_space':
                k.add_node_k(node)
            elif node.node_type == 'work_space':
                k.add_node_k(node)
            elif node.node_type == 'bus_stop':
                k.add_node_k(node)
            elif node.node_type == 'hospital':
                k.add_node_k(node)
            else:
                pass

    def react(self, queryString):
        """
        React to a query string.

        Args:
            queryString (str): The query string.

        Returns:
            tuple: The action and arguments to perform.
        """
        query = f"{queryString}"
        action1 = []
        
        for x in self.knowledge.query(query):
            action1.append(x['Action'])
            action1.append(x['Arguments'])
            
        try:
            action = list(self.knowledge.query(query))[0]
            return action['Action'], action['Arguments']
        except:
            return None, None
    

class LocalPlanningLayer:
    """
    Class representing the local planning layer of an agent.

    Attributes:
        behavior_layer_based (BehaviorLayer): The behavior layer based on which the local planning is performed.
        prolog (Knowledge): The knowledge base of the agent.
    """
    def __init__(self, behavior_layer_based, knowledge: Knowledge):
        """
        Initialize the local planning layer.

        Args:
            behavior_layer_based (BehaviorLayer): The behavior layer based on which the local planning is performed.
            knowledge (Knowledge): The knowledge base of the agent.
        """
        self.behavior_layer_based = behavior_layer_based
        self.knowledge = knowledge
        self.plans = {} 

    def plan(self, queryString):
        """
        Plan based on a query string.

        Args:
            queryString (str): The query string.
        """
        query = f"{queryString}"
        list(self.knowledge.query(query))
        
        

class CooperativeLayer:
    """
    Class representing the cooperative layer of an agent.

    Attributes:
        local_planning_layer (LocalPlanningLayer): The local planning layer of the agent.
        prolog (Knowledge): The knowledge base of the agent.
    """
    def __init__(self, local_planning_layer, knowledge: Knowledge):
        """
        Initialize the cooperative layer.

        Args:
            local_planning_layer (LocalPlanningLayer): The local planning layer of the agent.
            knowledge (Knowledge): The knowledge base of the agent.
        """
        self.local_planning_layer = local_planning_layer
        self.knowledge = knowledge

    def cooperate(self, queryString):
        """
        Cooperate based on a query string.

        Args:
            queryString (str): The query string.
        """
        query = f"{queryString}"
        self.knowledge.query(query)
