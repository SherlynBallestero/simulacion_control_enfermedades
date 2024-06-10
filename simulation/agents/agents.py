import random
from typing import Dict, Any, Tuple, List, Set, Hashable
from simulation.enviroment.graph import Graph
from simulation.enviroment.sim_nodes import CitizenPerceptionNode as CPNode
from simulation.agents.agent_arquitecture import BehaviorLayer, LocalPlanningLayer, CooperativeLayer, Knowledge, KnowledgeCanelo
from ai.genetic_algorythm import GA
import logging

logger = logging.getLogger(__name__)

class Agent:
    """Class representing an agent in the simulation."""
    def __init__(self, 
                 unique_id: int,
                 mind_map: Graph,
                 status: str = 'susceptible',
                 bb_component: BehaviorLayer = None,
                 lp_component: LocalPlanningLayer = None,
                 c_component: CooperativeLayer = None,
                 wi_component: 'WorldInterface' = None,
                 knowledge_base: Knowledge = None
                 ):
                   
        # Agent Caracteristics
        self.location = -1
        self.unique_id = unique_id
        self.status = status
        self.age_group = random.choice(['young', 'adult', 'old'])
        self.masked = False
        self.vaccinated = False
        self._last_path = []

        # Hierarchical Knowlege Base
        # self.belief_system = belief_system if belief_system is not None else {}
        self.knowledge_base = knowledge_base
        self.mind_map = mind_map if mind_map is not None else {}
        self.symptoms = []
        self.hospitals = [node.id for node in mind_map.nodes.values() if node.node_type == 'hospital']
        self.public_places = [node.id for node in mind_map.nodes.values() if node.node_type == 'public_space']
        self.knowledge_base.facts['hospitals'] = self.hospitals
        self.knowledge_base.facts['public_places'] = self.public_places
        
        # Agent Control Unit
        self.bbc = bb_component
        self.pbc = lp_component
        self.cc = c_component
        self.wi = wi_component

    def process_perception(self, world_perception: Dict[Hashable, CPNode], step_num):
        k = self.knowledge_base
        k.add_date_k(format_day(step_num))
        
        for node in world_perception.values():
            old_perception = self.mind_map.nodes[node.id]
            new_perception = world_perception[node.addr]
            old_perception.capacity_status = new_perception.capacity_status
            old_perception.information_source = new_perception.information_source
            old_perception.mask_required = new_perception.mask_required
            k.add_node_k(new_perception)

    def step(self, step_num):
        perception = self.wi.percieve(self, step_num)
        self.process_perception(perception, step_num)
        action, arguments = self.bbc.react()#TODO: Im am here
        if action == 'idle':
            self.pbc.plan()
            action, arguments = self.bbc.react()
        # if action == 'idle':
        #     self.cc.cooperate(self, "coperate()")
        #     self.pbc.plan()
        #     action, arguments = self.bbc.react()
        # if (not action)  :
        #     coperate = self.cc.cooperate(self, "coperate()")

        # log_agent_intentions(self.knowledge_base)
        self.wi.act(self, action, arguments)
        self.knowledge_base.feedback(self.location, self.masked)
        
    def recieve_message(self, sender: int, message: any, message_type: str):
        
        if (sender not in self.knowledge_base['friends']) and (sender != -1):
            return
        
        if message_type == 'map':
            self._get_map_info(message['location'], message['info'], message['value'])
        if message_type == 'measure':
            self._get_measure_info(message['info'], message['value'])

    def _get_map_info(self, location, info, value):
        self.mind_map.nodes[location].__dict__[info] = value
        
    def _get_measure_info(self, measure, value):
        self.knowledge_base.facts[measure] = value

class Canelo:
    """Class representing the president."""
    def __init__(self, 
                 mind_map: Graph,
                 bb_component: BehaviorLayer = None,
                 lp_component: LocalPlanningLayer = None,
                 c_component: CooperativeLayer = None,
                 wi_component: 'WorldInterfaceCanelo' = None,
                 knowledge_base: KnowledgeCanelo = None,
                 solution: list = [0]*9
                 ):
        self.unique_id = -1

        # Hierarchical Knowlege Base
        self.knowledge_base = knowledge_base
        self.mind_map = mind_map if mind_map is not None else {}
        
        self.measures = ['mask_use', 'social_distancing', 'tests_and_diagnosis', 'contact_tracing', 'vaccination', 'quarantine', 'temporary_closure_pp', 'temporary_closure_work']
        self.taken_measures = []

        # Agent Control Unit
        self.bbc = bb_component
        self.pbc = lp_component
        self.cc = c_component
        self.wi = wi_component
        
        self.solution = solution
        self.budget = 100000
        self.cost = {
            'mask_use':1, 
            'social_distancing':0.5, 
            'tests_and_diagnosis':2, 
            'contact_tracing':3, 
            'vaccination':3, 
            'quarantine':4, 
            'temporary_closure_pp':5, 
            'temporary_closure_work':5
        }

    def step(self, infected_agents):
        x = infected_agents / len(self.wi.list_agents)
        
        for i in self.taken_measures:
            self.budget -= self.cost[i]
            
        action = self.recommendation_based_on_severity(x, self.solution)
        self.wi.act(self,action)
        
    def recommendation_based_on_severity(self,people_sick, solution:list):
        try:
            if not solution:
                return 'nothing'
        except:
            pass
        
        if people_sick >= solution[0] and not 'mask_use' in  self.taken_measures:
            self.taken_measures.append('mask_use')
            return 'mask_use'
        elif people_sick >= solution[1] and not 'social_distancing' in  self.taken_measures:
            self.taken_measures.append('social_distancing')
            return 'social_distancing'
        elif people_sick >= solution[2] and not 'tests_and_diagnosis' in  self.taken_measures:
            self.taken_measures.append('tests_and_diagnosis')
            return 'tests_and_diagnosis'
        elif people_sick >= solution[3] and not 'contact_tracing' in  self.taken_measures:
            self.taken_measures.append('contact_tracing')
            return 'contact_tracing'
        elif people_sick >= solution[4] and not 'vaccination' in  self.taken_measures:
            self.taken_measures.append('vaccination')
            return 'vaccination'
        elif people_sick >= solution[5] and not 'quarantine' in  self.taken_measures:
            self.taken_measures.append('quarantine')
            return 'quarantine'
        elif people_sick >= solution[6] and not 'temporary_closure_pp' in  self.taken_measures:
            self.taken_measures.append('temporary_closure_pp')
            return 'temporary_closure_pp'
        elif people_sick >= solution[7] and not 'temporary_closure_work' in  self.taken_measures:
            self.taken_measures.append('temporary_closure_work')
            return 'temporary_closure_work'
        else:
            return 'nothing'
        
 
def log_agent_intentions(agent_k):
    logger.info(f'Agent Intent:')
    intention_1 = list(agent_k.query(f'goal(G)'))
    intention_2 = list(agent_k.query(f'goal(G, P)'))
    if intention_1:
        logger.info(f'\tgoal: {intention_1[0]["G"]}')
    if intention_2:
        logger.info(f'\tgoal: {intention_2[0]["G"]}, parameters: {intention_2[0]["P"]}')
    if not intention_1 and not intention_2:
        logger.info(f'\tgoal: The agent has not goals in life :-(')

def format_day(step_num):
    # Calculating day of the week, hour and min sim_days = 31 sim_hours = sim_days * 24 sim_steps = sim_hours * 6
    days_of_the_week = [ "monday", "tuesday", "wednesday", "thursday", "friday", "saturday","sunday"]
    min = step_num % 6 * 10
    hour = step_num // 6 % 24
    day = step_num // 6 // 24 % 7
    week_day = days_of_the_week[day]
    month_day = step_num // 6 // 24
    return week_day, month_day, hour, min
