from pyswip import Prolog
import random

class Knowledge:
    def __init__(self):
        self.prolog = Prolog()
        self.prolog.consult('hierarchical_agent_KB.pl')
        
    def add_date_k(self, date):
        list(self.prolog.query(f'add_date({date[0]},{date[1]},{date[2]},{date[3]})'))
        
    def add_symptom_k(self, s):
        list(self.prolog.query(f'add_symptom({s})'))
    
    def add_hospital_k(self, h):
        list(self.prolog.query(f'add_hospital({h})'))
        
class BehaviorLayer:
    def __init__(self, world_model, knowledge):
        self.world_model = world_model
        self.prolog = Prolog()
        self.prolog.consult('hierarchical_agent_KB.pl')

    def react(self, queryString):
        query = f"{queryString}"
        action = []
        for result in self.prolog.query(query):
            action.append(result['FunctionName'])
            action.append(result['Args'])
            
        # if not actions:
        #     action = self.chose_action(actions)
       
        try:
            return action[0], action[1]
        except:
            return None, None
    

class LocalPlanningLayer:
    def __init__(self, behavior_layer_based):
        self.behavior_layer_based = behavior_layer_based
        self.prolog = Prolog()
        self.prolog.consult('hierarchical_agent_KB.pl')
        self.plans = {} # Dictionary of plans

    def plan(self, queryString):
        query = f"{queryString}"
        self.prolog.query(query)

class CooperativeLayer:
    def __init__(self, local_planning_layer):
        self.local_planning_layer = local_planning_layer
        self.prolog = Prolog()
        self.prolog.consult('hierarchical_agent_KB.pl')

    def cooperate(self, queryString):
        query = f"{queryString}"
        self.prolog.query(query)