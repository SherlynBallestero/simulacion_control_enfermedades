from pyswip import Prolog
from typing import Tuple
import random
from simulation.enviroment.sim_nodes import *
from simulation.enviroment.graph import Graph

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
        self.facts = {}
        self.initializing_k()

    def add_node_k(self, node: SimNode):
        
        node_info = {
            'addr': node.addr,
            'capacity_status': node.capacity_status,
            'node_type': node.node_type,
            'mask_required': node.mask_required
        }#TODO: add if the place is open
        try:
            node_info['oppening_hours'] = node.oppening_hours,
            node_info['closing_hours'] = node.closing_hours
        except:
            pass
            
        if "map" in self.facts:
            self.facts['map'][node.id] = node_info
        else: 
            self.facts['map'] = {
                node.id: node_info
            } 

    def add_date_k(self, date):
        """
        Add a date to the knowledge base.

        Args:
            date (tuple): The date to add.
        """
        self.facts['date'] = {
            'week_day': date[0],
            'day': date[1],
            'hour': date[2],
            'min': date[3] 
        }

    def add_symptom_k(self, symptom):
        """
        Add a symptom to the knowledge base.

        Args:
            symptom (str): The symptom to add.
        """
        list(self.prolog.query(f'add_symptom({symptom})'))
        
        if 'symptoms' in self.facts:
            self.facts['symptoms'].add(symptom)
        else:
            self.facts['symptoms'] = set()

    def add_hospital_k(self, hospital_id: int, hospital_addr: Tuple[int,int]):
        """
        Add a hospital to the knowledge base.

        Args:
            hospital_id (int): The identifier of the hospital.
            hospital_addr (str): The address of the hospital.
        """
        # list(self.prolog.query(f'add_hospital({hospital_id}, {hospital_addr})'))
        raise not NotImplementedError()

    def add_home(self, home_id: int):
        """
        Add a home to the knowledge base.

        Args:
            home_id (int): The identifier of the home.
        """
        self.facts['home'] = home_id

    def add_work_place(self, node):
        """
        Add a workplace to the knowledge base.

        Args:
            wp_id (int): The identifier of the workplace.
        """
        self.facts['work_place'] = {
            'id': node.id,
            'addr':node.addr,
            'opening_hours': node.opening_hours,
            'closing_hours': node.closing_hours,
            'is_open': node.is_open
        }

    def add_message(self, remitent, message):
        pass

    def add_open_place(self, id: int, open: bool):
        """
        Add an open place to the knowledge base.

        Args:
            id (int): The identifier of the place.
            open (bool): Whether the place is open.
        """
        self.facts['open_place'] = {
            'id': id,
            'open': open
        }

    def add_open_hours_place(self, id: int, opening_hours: int, closing_hours: int):
        """
        Add open hours to the knowledge base.

        Args:
            id (int): The identifier of the place.
            opening_hours (int): The opening hours of the place.
            closing_hours (int): The closing hours of the place.
        """
        self.facts['open_hours_place'] = {
            'id': id,
            'opening_hours': opening_hours,
            'closing_hours': closing_hours
        }

    def add_dissease_symptoms(self, symptom_list: list):
        """
        Add disease symptoms to the knowledge base.

        Args:
            symptom_list (list): The list of symptoms.
        """
        # list(self.prolog.query(f'add_dissease_symptoms({symptom_list})'))
        raise NotImplementedError()

    def add_current_location(self, location_id: int):
        """
        Add current location id

        Args:
            location_id (int): The id of the node the agent is currently in
        """
        self.facts['location'] = location_id

    def add_is_medical_personnel(self, medical_personnel: bool):
        """
        Add medical personnel information to the knowledge base.

        Args:
            medical_personnel (bool): Whether the agent is medical personnel.
        """
        self.facts['is_medic'] = medical_personnel
        
    def vaccination_k(self, bool: bool):
        """
        Add vaccination to the knowledge base.
        """
        self.facts['vaccination_necessity'] = bool

    def add_mask_necessity(self, mask_necessity: bool):
        """
        Add mask necessity information to the knowledge base.

        Args:
            mask_necessity (bool): Whether a mask is necessary.
        """
        self.facts['mask_necessity'] = mask_necessity

    def add_mask_requirement(self, place_id: int, requirement: bool):
        """
        Add mask requirement information to the knowledge base.

        Args:
            place_id (int): The identifier of the place.
            requirement (bool): Whether a mask is required.
        """
        # list(self.prolog.query(f'add_place_to_use_mask({place_id}, {requirement})'))
        if 'map' in self.facts and place_id in self.facts['map']:
            self.facts['maps'][place_id]['mask_required'] = requirement
            

    def add_social_distancing(self, requirement: bool):
        self.facts['social_distancing'] = requirement

    def add_tests_and_diagnosis(self, requirement: bool):
        self.facts['tests_and_diagnosis'] = requirement

    def add_friends(self, friend_list: list):
        # if friend_list:
        #     list(self.prolog.query(f'add_friends({friend_list})'))
        if 'friends' in self.facts:
            self.facts['friends'].union(friend_list)
        else:
            self.facts['friends'] = set(friend_list)

    def add_wearing_mask(self, wearing_mask: bool):
        self.facts['wearing_mask'] = wearing_mask

    def add_quarantine(self, quarantine: bool):
        self.facts['quarantine'] = quarantine

    def add_location(self, location: int):
        self.facts['location'] = location

    def feedback(self, location, wearing_mask):
        self.add_location(location)
        self.add_wearing_mask(wearing_mask)

    def initializing_k(self):
        self.facts['goal'] = 'none'
        self.facts['goal_parameters'] = []
        self.facts['wearing_mask'] = False
        self.facts['too_sick'] = False
        self.facts['mask_necessity'] = False
        self.facts['medical_check'] = False
        self.facts['social_distancing'] = False
        self.facts['messages'] = []
        self.facts['vaccinated'] = False
        self.facts['vaccination_necessity'] = False
        self.facts['friends'] = set()

    def update_goals(self, mind_map: Graph = None):
        # removes already achieved goals
        if self.facts['goal'] == 'vaccination' and self.facts['vaccinated']:
            self.facts['goal'] = 'none'
        if self.facts['goal'] == 'wear_mask' and self.facts['wearing_mask']:
            self.facts['goal'] = 'none'
        if self.facts['goal'] == 'remove_mask' and not self.facts['wearing_mask']:
            self.facts['goal'] = 'none'
        if (self.facts['goal'] == 'move' and self.facts['location'] == self.facts['goal_parameters'][0]):
            self.facts['goal'] = 'none'
            self.facts['goal_parameters'] = []
        if (self.facts['goal'] == 'move' and mind_map[self.facts['goal_parameters'][0]].node_type not in  ['block', 'house'] and not mind_map[self.facts['goal_parameters'][0]].is_open):
            self.facts['goal'] = 'none'
            self.facts['goal_parameters'] = []
    
    def __getitem__(self, index):
        return self.facts[index]

class KnowledgeCanelo:
    """
    Class representing the knowledge base of canelo.

    Attributes:
        prolog (Prolog): The Prolog engine for querying the knowledge base.
    """
    def __init__(self):
        """
        Initialize the knowledge base.
        """
        pass
        
    def query(self, queryString):
        """
        Query the knowledge base.

        Args:
            queryString (str): The query string.

        Returns:
            list: The results of the query.
        """
        action = list(self.knowledge.query(queryString))[0]
        return action['Recommendation'], action['RecomendationPlaces']

class BehaviorLayer:
    """
    Class representing the behavior layer of an agent.

    Attributes:
        world_model (Graph): The world model of the agent.
        knowledge (Knowledge): The knowledge base of the agent.
    """
    def __init__(self, world_model, knowledge: Knowledge, mind_map: Graph):
        """
        Initialize the behavior layer.

        Args:
            world_model (Graph): The world model of the agent.
            knowledge (Knowledge): The knowledge base of the agent.
        """
        self.world_model = world_model
        self.knowledge = knowledge
        self.mind_map = mind_map
        try:
            self.add_map_to_k()
        except:
            pass

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

    def react(self):
        """
        React to a query string.

        Args:
            queryString (str): The query string.   

        Returns:    
            tuple: The action and arguments to perform.
        """
        kb = self.knowledge
        mm = self.mind_map
        kb.update_goals(mm)
        if (kb['mask_necessity'] and mm[kb['location']].mask_required and (not kb['wearing_mask'])):
            return 'wear_mask', []
        
        if ((not mm[kb['location']].mask_required) and kb['wearing_mask']):
            return 'remove_mask', []
        
        if (kb['goal'] == 'vaccination' and mm[kb['location']].node_type == 'hospital'):
            return 'get_vaccinated', [kb['location']]
        
        if (kb['medical_check']):
            return 'medical_check', []
        
        if (kb['goal'] == 'move' and kb['location'] != kb['goal_parameters'][0]):
            return 'move', (kb['goal_parameters'][0], kb['social_distancing'])
        
        if (kb['goal'] == 'send_message'):
            return 'send_message', kb['goal_parameters'][0]
        return 'idle', []

    def _split_string(self, s):
        parts = s.split('(', 1)
        outside_parentheses = parts[0]
        inside_parentheses = parts[1].split(')', 1)[0] if len(parts) > 1 else ''
        return outside_parentheses, inside_parentheses
    

class LocalPlanningLayer:
    """
    Class representing the local planning layer of an agent.

    Attributes:
        behavior_layer_based (BehaviorLayer): The behavior layer based on which the local planning is performed.
        prolog (Knowledge): The knowledge base of the agent.
    """
    def __init__(self, behavior_layer_based: BehaviorLayer, knowledge: Knowledge, mind_map: Graph):
        """
        Initialize the local planning layer.

        Args:
            behavior_layer_based (BehaviorLayer): The behavior layer based on which the local planning is performed.
            knowledge (Knowledge): The knowledge base of the agent.
        """
        self.behavior_layer_based = behavior_layer_based
        self.knowledge = knowledge
        self.plans = {} 
        self.mind_map = mind_map

    def plan(self):
        """
        Plan based on a query string.

        Args:
            queryString (str): The query string.
        """
        kb = self.knowledge
        mm = self.mind_map
        date = kb['date']
        open_place = self._pp_is_open(mm, kb['public_places'], date['week_day'], date['hour'])
        kb.update_goals(mm)

        # Get Vaccine Routine
        if (kb['vaccination_necessity'] and (not kb['vaccinated'])):
            self.vaccination_routine()

        # Dissease Checking Routine
        elif (kb['too_sick']):
            self.hospital_routine()

        # Work Routine
        elif (self._work_is_open(mm, kb['work_place'], date['week_day'], date['hour']) and (not kb['too_sick'])):
            self.work_day_routine(kb['work_place'])

        # Entertainment Routine
        elif (open_place and (not kb['too_sick'])):#((public_space(Id, _),open_place(Id, true), go_public_place_rutine(Id));  Plan = no_pweek_day(W), (W == saturday; W == sunday)) -> go_public_place_rutine(Id), Plan = lan.
            self.entertainment_routine(open_place)

        # Return Home
        elif (kb['location'] != kb['home']):
            kb.facts['goal'] = 'move'
            kb.facts['goal_parameters'] = [kb['home']]

    def vaccination_routine(self):
        kb = self.knowledge
        kb.facts['goal'] = 'move'
        target_hospital = self._open_hospitals(self.mind_map)[0]
        kb.facts['goal_parameters'] = [target_hospital]

        if kb.facts['location'] == target_hospital:
            kb.facts['goal'] = 'vaccination'
            kb.facts['goal_parameters'] = []
            
    def entertainment_routine(self, public_place):# TODO: Fix agents moving all weekend
        kb = self.knowledge
        
        kb.facts['goal'] = 'move'
        kb.facts['goal_parameters'] = [public_place]
        
        if kb.facts['location'] == public_place:
            kb.facts['goal'] = 'have_fun'
            kb.facts['goal_parameters'] = []
        
        time_to_go_home = self.mind_map[public_place].closing_hours
        if time_to_go_home == kb.facts['date']['hour']:
            home = kb.facts['home'] 
            kb.facts['goal'] = 'move'
            kb.facts['goal_parameters'] = [home]

    def work_day_routine(self, work):
        kb = self.knowledge 
        kb.facts['goal'] = 'move'
        kb.facts['goal_parameters'] = [work['id']]
        
        if kb.facts['location'] == work['id']:
            kb.facts['goal'] = 'work'
            kb.facts['goal_parameters'] = []
        
        time_to_go_home = kb.facts['work_place']['closing_hours']
        if time_to_go_home == kb.facts['date']['hour']:
            home = kb.facts['home'] 
            kb.facts['goal'] = 'move'
            kb.facts['goal_parameters'] = [home]

    def hospital_routine(self, hospital):
        kb = self.knowledge
        kb.facts['goal'] = 'move'
        kb.facts['goal_parameters'] = [hospital]
        
        if kb.facts['location'] == hospital:
            kb.facts['goal'] = 'recibe_atencion_medica'
            kb.facts['goal_parameters'] = []

    def _open_hospitals(self, mind_map):
        hospitals = []
        for node in mind_map.nodes.values():
            if node.node_type == 'hospital' and node.is_open:
                hospitals.append(node.id)
        return hospitals

    def _work_is_open(self, mm, work_info, week_day, hour):
        return (not (week_day in ['saturday', 'sunday'])) and (work_info['opening_hours'] <= hour) and (hour <= work_info['closing_hours']) and mm[work_info['id']].is_open
    
    def _pp_is_open(self, mm, public_places, week_day, hour):
        if not(week_day in ['saturday', 'sunday']):
            return
        open_places = [(mm[public_place].is_open, mm[public_place].id, mm[public_place].oppening_hours, mm[public_place].closing_hours) for public_place in public_places]
        for is_open, public_place, opens, closes in random.sample(open_places, len(open_places)):
            if is_open and opens <= hour and hour <= closes:
                return public_place
        return
    
    def _open_public_places(self, mind_map):
        raise NotImplementedError()

    def plan_coperative(self, agent, plan):
        self.behavior_layer_based.search_friend(agent, plan)

class CooperativeLayer:
    """
    Class representing the cooperative layer of an agent.

    Attributes:
        local_planning_layer (LocalPlanningLayer): The local planning layer of the agent.
        prolog (Knowledge): The knowledge base of the agent.
    """
    def __init__(self, local_planning_layer, knowledge: Knowledge, mind_map: Graph):
        """
        Initialize the cooperative layer.

        Args:
            local_planning_layer (LocalPlanningLayer): The local planning layer of the agent.
            knowledge (Knowledge): The knowledge base of the agent.
        """
        self.local_planning_layer: LocalPlanningLayer = local_planning_layer
        self.knowledge = knowledge
        self.mind_map = mind_map

    def cooperate(self,agent, queryString):
        """
        Cooperate based on a query string.

        Args:
            queryString (str): The query string.
        """
        kb = self.knowledge
        mm = self.mind_map
        
        if not 'friends' in kb.facts:
            return

        friends = kb['friends']

        public_places = self._get_public_places()

