from typing import Dict, Any, Tuple, List, Set
import random 
from utils.graph import Graph,Node
# from agent_arquitecture import WorldInterface, BehaviorLayerBased, LocalPlanningLayer, CooperativeLayer

class Agent:
    """Class representing an agent in the simulation."""
    def __init__(self, unique_id: int, belief_system: Dict[str, Any] = None,
                 knowledge_base: Dict[str, List[Any]] = None,
                 mind_map: Dict[str, Set[str]] = None,
                 status: str = 'susceptible',
                 daily_route: List[Tuple[float, float]] = None):
        """
        Initialize the agent.

        Args:
            unique_id (int): Unique identifier for the agent.
            belief_system (Dict[str, Any], optional): Dictionary representing the agent's belief system. Defaults to None.
            knowledge_base (Dict[str, List[Any]], optional): Dictionary representing the agent's knowledge base. Defaults to None.
            mind_map (Dict[str, Set[str]], optional): Dictionary representing the agent's mind map. Defaults to None.
        """
        self.unique_id = unique_id
        self.belief_system = belief_system if belief_system is not None else {}
        self.knowledge_base = knowledge_base if knowledge_base is not None else {}
        self.mind_map = mind_map if mind_map is not None else {}
        self.status = status
        self.daily_route = daily_route if daily_route is not None else []

        # Inicialización de la arquitectura interrap
        # self.world_interface = WorldInterface(self.mind_map, self.perception_module, self.action_module)
        # self.behavior_layer_based = BehaviorLayerBased(self.mind_map)
        # self.local_planning_layer = LocalPlanningLayer(self.behavior_layer_based)
        # self.cooperative_layer = CooperativeLayer(self.local_planning_layer)

    def update_belief(self, belief: str, value: Any) -> None:
        """
        Update a belief in the agent's belief system.

        Args:
            belief (str): The belief to be updated.
            value (Any): The new value of the belief.
        """
        self.belief_system[belief] = value
        # After updating a belief, the agent might need to re-evaluate its actions or plans
        self.react_to_belief_change(belief, value)

    def add_knowledge(self, topic: str, information: Any) -> None:
        """
        Add knowledge to the agent's knowledge base.

        Args:
            topic (str): The topic of the knowledge.
            information (Any): The information to be added.
        """
        if topic not in self.knowledge_base:
            self.knowledge_base[topic] = []
        self.knowledge_base[topic].append(information)

    def update_mind_map(self, concept: str, related_concepts: Set[str]) -> None:
        """
        Update the agent's mind map with related concepts.

        Args:
            concept (str): The concept to be updated.
            related_concepts (Set[str]): The set of related concepts.
        """
        if concept not in self.mind_map:
            self.mind_map[concept] = set()
        self.mind_map[concept].update(related_concepts)

    def learn(self, new_information: Dict[str, Any]) -> None:
        """
        Learn new information and update beliefs, knowledge, and mind map accordingly.

        Args:
            new_information (Dict[str, Any]): Dictionary containing new information.
        """
        # Update beliefs, knowledge, mind map based on new information
        pass

    def act(self, perception: list[Node]) -> dict[str,any]:
        """Define agent's actions based on beliefs, knowledge, and mind map."""

        adj_nodes = [adj_node.id for adj_node in perception]
        return "move", random.choice(adj_nodes)
    
    def move_to_next_location(self):
        if self.daily_route:
            next_location = self.daily_route.pop(0)
            self.location = next_location
        pass
            
    def find_safe_location(self):
        """
        Encuentra un lugar seguro para el agente infectado.
        """
        # Lógica para encontrar un lugar seguro
        pass

    def communicate(self, other_agent: 'Agent', message: dict) -> None:
        """
        Communicate with another agent by sharing information.

        Args:
            other_agent (Agent): The agent to communicate with.
            message (dict): The information to share.
        """
        # Example: Share information about a disease outbreak
        if 'disease_outbreak' in message:
            other_agent.update_belief('disease_outbreak', message['disease_outbreak'])

         # Ejemplo de interacción: compartir información sobre la enfermedad
        if self.status == 'infected' and other_agent.status == 'susceptible':
            self.share_information(other_agent)

    def react_to_belief_change(self, belief: str, value: Any) -> None:
        """
        React to a change in a belief. This could involve updating plans, re-evaluating actions, etc.

        Args:
            belief (str): The belief that has changed.
            value (Any): The new value of the belief.
        """
        if belief == 'location_safety':
            # Si la creencia es sobre la seguridad de una ubicación,
            # el agente podría reevaluar su plan de navegación.
            self.reevaluate_navigation_plan(belief, value)
        elif belief == 'disease_outbreak':
            # Si la creencia es sobre un brote de enfermedad,
            # el agente podría cambiar su plan para evitar áreas afectadas.
            self.adjust_plan_for_disease_outbreak(belief, value)
        else:
            # Para otras creencias, el agente podría simplemente actualizar su plan existente.
            self.update_plan(belief, value)

    def reevaluate_navigation_plan(self, belief: str, value: Any) -> None:
        """
        Reevaluate the navigation plan based on the new belief value.
        """
        # Implementa la lógica para reevaluar el plan de navegación aquí
        pass

    def adjust_plan_for_disease_outbreak(self, belief: str, value: Any) -> None:
        """
        Adjust the plan to avoid areas affected by a disease outbreak.
        """
        # Implementa la lógica para ajustar el plan en respuesta a un brote de enfermedad aquí
        pass

    def update_plan(self, belief: str, value: Any) -> None:
        """
        Update the existing plan based on the new belief value.
        """
        # Implementa la lógica para actualizar el plan existente aquí
        pass

    def perceive(self):
        # Llama al método perceive del módulo de percepción
        self.world_interface.perceive()

    def plan(self, goal):
        # Llama al método plan del módulo de planificación
        self.local_planning_layer.plan(goal)

    def cooperate(self, goal):
        # Llama al método cooperate del módulo de cooperación
        self.cooperative_layer.cooperate(goal)

class RegentOrgAgent(Agent):
    def __init__(self):
        pass

class CitizenAgent(Agent):
    def __init__(self, unique_id: int, belief_system: Dict[str, Any] = None, knowledge_base: Dict[str, List[Any]] = None, mind_map: Dict[str, Set[str]] = None, status: str = 'susceptible'):
        pass

class HealthPersonalAgent(CitizenAgent):
    def __init__(self, unique_id: int, belief_system: Dict[str, Any] = None, knowledge_base: Dict[str, List[Any]] = None, mind_map: Dict[str, Set[str]] = None, status: str = 'susceptible'):
        pass
        

if __name__ == '__main__':
    # Example usage
    belief_system = {'trust': 0.8, 'risk_awareness': 0.6, "schedule": [
        (16,"Park"),(19,"Restaurant"),(20,"Bar"),
        ]
                     }
    knowledge_base = {'epidemics': ['definition', 'spread mechanisms']}
    mind_map = {'epidemics': {'pandemics', 'outbreaks'}}
    agent = Agent(1, belief_system, knowledge_base, mind_map)
