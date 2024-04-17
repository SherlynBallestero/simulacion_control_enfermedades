from pyswip import Prolog
import random

class Knowledge:
    def __init__(self):
        self.prolog = Prolog()
        self.prolog.consult('./simulation/agents/hierarchical_agent_KB.pl')
        
    def add_node_k(self, node):
        list(self.prolog.query())
        
    def add_date_k(self, date):
        list(self.prolog.query(f'add_date({date[0]},{date[1]},{date[2]},{date[3]})'))
        
    def add_symptom_k(self, symptom):
        list(self.prolog.query(f'add_symptom({symptom})'))
    
    def add_hospital_k(self, hospital_id, hospital_addr):
        list(self.prolog.query(f'add_hospital({hospital_id}, {hospital_addr})'))
        
    def add_home(self, home_id):
        list(self.prolog.query(f'add_home({home_id})'))
    
    def add_work_place(self, wp_id):
        list(self.prolog.query(f'add_work_place({wp_id})'))
    
    def add_open_place(self, id, open):
        list(self.prolog.query(f'add_open_place({id}, {str(open).lower()})'))
    
    def add_open_hours(self, id, opening_hours, closing_hours):
        list(self.prolog.query(f'add_open_hours_place({id}, {opening_hours}, {closing_hours})'))
    
    def add_dissease_symptoms(self, symptom_list: list):
        list(self.prolog.query(f'add_dissease_symptoms({symptom_list})'))
    
    def add_is_medical_personnel(self, medical_personnel):
        list(self.prolog.query(f'add_if_is_medical_personal({medical_personnel})'))
    
    def add_mask_necessity(self, mask_necessity):
        list(self.prolog.query(f'add_mask_necessity({mask_necessity})'))
    
    def add_mask_requirement(self, place_id, requirement):
        list(self.prolog.query(f'add_place_to_use_mask({place_id}, {requirement})'))
    
    def query(self, queryString):
        return []
        
class BehaviorLayer:
    def __init__(self, world_model, knowledge: Knowledge):
        self.world_model = world_model
        self.knowlege = knowledge
        self._add_map_to_k()

    def add_map_to_k(self):
        pass

    def react(self, queryString):
        query = f"{queryString}"
        action = []
        for result in self.knowlege.query(query):
            action.append(result['FunctionName'])
            action.append(result['Args'])
            
        # if not actions:
        #     action = self.chose_action(actions)
       
        try:
            return action[0], action[1]
        except:
            return None, None
    

class LocalPlanningLayer:
    def __init__(self, behavior_layer_based, knoeledge: Knowledge):
        self.behavior_layer_based = behavior_layer_based
        self.prolog = Knowledge
        self.plans = {} # Dictionary of plans

    def plan(self, queryString):
        query = f"{queryString}"
        self.prolog.query(query)

class CooperativeLayer:
    def __init__(self, local_planning_layer, knowledge: Knowledge):
        self.local_planning_layer = local_planning_layer
        self.prolog = knowledge

    def cooperate(self, queryString):
        query = f"{queryString}"
        self.prolog.query(query)