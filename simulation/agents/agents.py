import random
from typing import Dict, Any, Tuple, List, Set, Hashable
from simulation.enviroment.graph import Graph
from simulation.enviroment.sim_nodes import CitizenPerceptionNode as CPNode
from simulation.agents.agent_arquitecture import BehaviorLayer, LocalPlanningLayer, CooperativeLayer, Knowledge, KnowledgeCanelo
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
            k.add_node_k(new_perception)

    def step(self, step_num):
        perception = self.wi.percieve(self, step_num)
        self.process_perception(perception, step_num)
        action, arguments = self.bbc.react("behavioral_step(Action, Arguments)")
        if not action:
            plan = self.pbc.plan("planification_step(X)")
            action, arguments = self.bbc.react("behavioral_step(Action, Arguments)")
        
        # if (not action) and (not plan) :
        #     coperate = self.cc.cooperate(self, 'other', "coperate()")

        log_agent_intentions(self.knowledge_base)
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
                 knowledge_base: KnowledgeCanelo = None
                 ):

        # Hierarchical Knowlege Base
        self.knowledge_base = knowledge_base
        self.mind_map = mind_map if mind_map is not None else {}

        # Agent Control Unit
        self.bbc = bb_component
        self.pbc = lp_component
        self.cc = c_component
        self.wi = wi_component
 
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
        action, actionPlace = self.knowledge_base.query(f'recommendation_based_on_severity({x}, Recommendation, RecomendationPlaces)')
        self.wi.act(self,action, actionPlace)
        
 
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
