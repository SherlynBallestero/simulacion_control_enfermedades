import random
from typing import Dict, Any, Tuple, List, Set, Hashable
from utils.graph import Graph
from simulation.utils.sim_nodes import CitizenPerceptionNode as CPNode
from simulation.agents.agent_arquitecture import BehaviorLayer, LocalPlanningLayer, CooperativeLayer

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
                 knowledge_base: Dict[Hashable, Any] = None
                 ):
        """
        """
        # Agent Caracteristics
        self.unique_id = unique_id
        self.status = status
        self.age_group = random.choice(['young', 'adult', 'old'])

        # Hierarchical Knowlege Base
        # self.belief_system = belief_system if belief_system is not None else {}
        self.knowledge_base = knowledge_base if knowledge_base is not None else {}
        self.mind_map = mind_map if mind_map is not None else {}
        self.symptoms = []

        # Agent Control Unit
        self.bbc = bb_component
        self.pbc = lp_component
        self.cc = c_component
        self.wi = wi_component

    def process_perception(self, world_perception: Dict[Hashable, CPNode]):
        for node_id in world_perception.keys():
            old_perception = self.mind_map.nodes[node_id]
            new_perception = world_perception[node_id]
            old_perception.capacity_status = new_perception.capacity_status
            old_perception.information_source = new_perception.information_source

    def step(self):
        perception = self.wi.percieve(self)
        self.process_perception(perception)
        action, arguments = self.bbc.react()
        self.wi.act(self, action, arguments)
        pass