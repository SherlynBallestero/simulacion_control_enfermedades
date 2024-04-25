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
        if action == 'idle':
            self.cc.cooperate(self, "coperate()")
            self.pbc.plan()
            action, arguments = self.bbc.react()
        # if (not action)  :
        #     coperate = self.cc.cooperate(self, "coperate()")

        # log_agent_intentions(self.knowledge_base)
        self.wi.act(self, action, arguments)
        self.knowledge_base.feedback(self.location, self.masked)
        
class Canelo:
    """Class representing the president."""
    def __init__(self, 
                 mind_map: Graph,
                 bb_component: BehaviorLayer = None,
                 lp_component: LocalPlanningLayer = None,
                 c_component: CooperativeLayer = None,
                 wi_component: 'WorldInterfaceCanelo' = None,
                 knowledge_base: KnowledgeCanelo = None,
                 solution: list = [0]*7
                 ):

        # Hierarchical Knowlege Base
        self.knowledge_base = knowledge_base
        self.mind_map = mind_map if mind_map is not None else {}
        
        self.measures = ['mask_use', 'social_distancing', 'tests_and_diagnosis', 'contact_tracing', 'vaccination', 'isolation', 'quarantine']
        self.measures_places = ['use_mask_pp', 'temporary_closure_pp', 'use_mask_work', 'temporary_closure_work']
        
        # Agent Control Unit
        self.bbc = bb_component
        self.pbc = lp_component
        self.cc = c_component
        self.wi = wi_component
        
        self.solution = solution
 
    def step(self, infected_agents):
        # perception = self.wi.percieve(self, step_num)
        # self.process_perception(perception, step_num)
        # action, arguments = self.bbc.react("behavioral_step(Action, Arguments)")

        # if not action:
        #     plan = self.pbc.plan("planification_step()")
        #     action, arguments = self.bbc.react("behavioral_step(Action, Arguments)")
        # log_agent_intentions(self.knowledge_base)
        
        # self.wi.act(self, action, arguments)
        # self.knowledge_base.feedback(self.location, self.masked)

        x = infected_agents * 0.1
        # action, actionPlace = self.knowledge_base.query(f'recommendation_based_on_severity({x}, Recommendation, RecomendationPlaces)')
        
        action = self.recommendation_based_on_severity(x, self.solution )
        self.wi.act(self,action)
        
    def recommendation_based_on_severity(self,people_sick, solution):
        
        # limits =  [limit_mask_use, limit_social_distancing,limit_tests_and_diagnosis, limit_contact_tracing, limit_vaccination, limit_isolation, limit_quarantine]

        # for x in solution:
        #     limits[x] = solution[x]
            
        if people_sick < solution[0]:
            return 'mask_use'
        elif people_sick < solution[1]:
            return 'social_distancing'
        elif people_sick < solution[2]:
            return 'tests_and_diagnosis'
        elif people_sick < solution[3]:
            return 'contact_tracing'
        elif people_sick < solution[4]:
            return 'vaccination'
        elif people_sick < solution[5]:
            return 'isolation'
        elif people_sick < solution[6]:
            return 'quarantine'
        else:
            return 'none'
        
 
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
