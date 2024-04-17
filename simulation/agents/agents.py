import random
from typing import Dict, Any, Tuple, List, Set, Hashable
from simulation.enviroment.graph import Graph
from simulation.enviroment.sim_nodes import CitizenPerceptionNode as CPNode
from simulation.agents.agent_arquitecture import BehaviorLayer, LocalPlanningLayer, CooperativeLayer, Knowledge
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
        self.unique_id = unique_id
        self.status = status
        self.age_group = random.choice(['young', 'adult', 'old'])
        self.masked = False
        self.vaccinated = False

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
        
        self.hour = 0
        self.day = 0
  

    def process_perception(self, world_perception: Dict[Hashable, CPNode], step_num):
        format_day = self.format_day(step_num)
        self.knowledge_base.add_date_k(format_day)
        
        for node in world_perception.values():
            old_perception = self.mind_map.nodes[node.id]
            new_perception = world_perception[node.addr]
            old_perception.capacity_status = new_perception.capacity_status
            old_perception.information_source = new_perception.information_source

    def step(self, step_num):
        perception = self.wi.percieve(self, step_num)
        self.process_perception(perception, step_num)
        action, arguments = self.bbc.react("detectar_sintomas(FunctionName, Args)")
        self.wi.act(self, action, arguments)
        
    def format_day(self, step_num):
        # 7 dias
        days_of_the_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        
        # formato fecha (dia semana, dia mes, hora)
        if step_num % 6 == 0 and step_num!= 0:
            self.hour = self.hour + 1
            
        if step_num % 144 == 0 and step_num != 0 :
            self.day = self.day + 1
             
        min = (step_num % 6) * 10
        week_day = days_of_the_week[self.day % 7]
        month_day = self.day % 31
        
        format = (week_day, month_day, self.hour, min)
        return format
