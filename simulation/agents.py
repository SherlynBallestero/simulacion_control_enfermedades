from typing import Dict, Any, Tuple, List, Set
import random 
from utils.graph import Graph,Node
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

    def update_belief(self, belief: str, value: Any) -> None:
        """
        Update a belief in the agent's belief system.

        Args:
            belief (str): The belief to be updated.
            value (Any): The new value of the belief.
        """
        self.belief_system[belief] = value

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
    
    def interact(self, other_agent: 'Agent') -> None:
        """
        Define interaction logic with other agents.

        Args:
            other_agent (Agent): The other agent to interact with.
        """
        # Ejemplo de interacción: compartir información sobre la enfermedad
        if self.status == 'infected' and other_agent.status == 'susceptible':
            self.share_information(other_agent)

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

    def find_information(self):
        """
        Busca información sobre la enfermedad.
        """
        # Lógica para buscar información
        pass
    
    def share_information(self, other_agent: 'Agent') -> None:
        """
        Comparte información sobre la enfermedad con otro agente.

        Args:
            other_agent (Agent): El agente con el que compartir información.
        """
        # Lógica para compartir información
        pass
    
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
