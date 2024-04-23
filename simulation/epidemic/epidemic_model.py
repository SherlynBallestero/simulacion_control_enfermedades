from simulation.agents.agents import Agent
from simulation.enviroment.graph import Graph
from pyswip import Prolog

from typing import List, Tuple
import random
import logging
import itertools
logger = logging.getLogger(__name__)

class EpidemicModel:
    """
    Class representing an epidemic model.

    Attributes:
        disease_k (Prolog): Prolog engine for querying disease progression.
        transmission_rate (float): The rate at which the disease is transmitted between agents.
        infection_stages (List[str]): The stages of infection.
        mask_effectiveness (float): The effectiveness of masks in preventing disease transmission.
        transmission_mask (float): The transmission rate adjusted for mask effectiveness.
    """
    def __init__(self, disease_description: str = './simulation/epidemic/chony_virus_progression.pl'):
        """
        Initialize the epidemic model.

        Args:
            disease_description (str, optional): Path to the Prolog file describing the disease progression. Defaults to './simulation/epidemic/chony_virus_progression.pl'.
        """
        self.disease_k = Prolog()
        self.disease_k.consult(disease_description)
        self.transmission_rate: float = list(self.disease_k.query('base_transmition_rate(R)'))[0]['R']
        self.infection_stages: List[str] = [atom.value for atom in list(self.disease_k.query('infection_stages(Stages)'))[0]['Stages']]
        self.mask_effectiveness: float = list(self.disease_k.query('mask_effectiveness(E)'))[0]['E']
        self.transmission_mask: float = self.transmission_rate * self.mask_effectiveness
        self.kill_agent = None

    def _query_stage(self, agent_id: int) -> str:
        """
        Query the current stage of an agent's infection.

        Args:
            agent_id (int): The unique identifier of the agent.

        Returns:
            str: The current stage of the agent's infection.
        """
        stage = list(self.disease_k.query(f'stage({agent_id}, S)'))
        return stage[0]['S'] if stage else None

    def _query_age_group(self, agent_id: int) -> str:
        """
        Query the age group of an agent.

        Args:
            agent_id (int): The unique identifier of the agent.

        Returns:
            str: The age group of the agent.
        """
        return list(self.disease_k.query(f'age_group({agent_id}, A)'))[0]['A']

    def _query_symptoms(self, agent_id: int) -> List[str]:
        """
        Query the symptoms of an agent.

        Args:
            agent_id (int): The unique identifier of the agent.

        Returns:
            List[str]: The symptoms of the agent.
        """
        result = list(self.disease_k.query(f'symptoms({agent_id}, S)'))
        return [atom.value for atom in result[0]['S']]

    def _step_dissease_query(self, agent: Agent) -> str:
        """
        Query the next stage of an agent's infection.

        Args:
            agent (Agent): The agent to query.

        Returns:
            str: The next stage of the agent's infection.
        """
        next_stage = list(self.disease_k.query(f'step({agent.unique_id}, S, Sy, St)'))[0]
        return next_stage['S']
    
    def step_dissease(self, agent: Agent) -> None:
        """
        Advance the agent's infection stage based on the disease progression rules.

        Args:
            agent (Agent): The agent to advance.
        """
        state = self._step_dissease_query(agent)
        if state in ['recovered', 'dead']:
            agent.status = state
            if state == 'dead':
                self.kill_agent(agent)
        else:
            self._update_agent(agent)

    def _infect_citizen(self, agent: Agent) -> None:
        """
        Infect an agent with the disease.

        Args:
            agent (Agent): The agent to infect.
        """
        query = f'add_agent({agent.unique_id}, {str(agent.vaccinated).lower()}, {agent.age_group})'
        list(self.disease_k.query(query))
        self._update_agent(agent)

    def _update_agent(self, agent: Agent) -> None:
        """
        Update an agent's status and symptoms based on the disease progression rules.

        Args:
            agent (Agent): The agent to update.
        """
        agent.status = self._query_stage(agent.unique_id)
        agent.symptoms = self._query_symptoms(agent.unique_id)

    def spread_disease(self, agent: Agent) -> None:
        """
        Spread the disease from one infected agent to another susceptible agent.

        Args:
            agent (Agent): The infected agent.
        """
        if random.random() < self.transmission_rate and agent.status not in ['dead', 'recovered']:
            self._infect_citizen(agent)

    def step(self, nodes: List[Tuple[List[Agent], float]]) -> None:
        """
        Perform a simulation step, where disease spreads and agents recover.

        Args:
            nodes (List[Tuple[List[Agent], float]]): The list of nodes in the simulation, each containing a list of agents and a contact rate.
        """
        contact_list = []
        for (citizens, contact_rate) in nodes:
            for citizen in citizens:
                if citizen.status in self.infection_stages:
                    agent_old_status = self._query_stage(citizen.unique_id)
                    agent_old_symptoms = self._query_symptoms(citizen.unique_id)
                    self.step_dissease(citizen)
                    # log the new state of the dissease and the symptoms
                    agent_new_status = self._query_stage(citizen.unique_id)
                    if agent_new_status in self.infection_stages:
                        agent_new_symptoms = self._query_symptoms(citizen.unique_id)
                        log_agent_symptoms_chages(agent_old_symptoms, agent_new_symptoms)
                    if agent_new_status != agent_old_status:
                        logger.info(f'Agent status changed from {agent_old_status} to {agent_new_status}')
                    
                    
                else:
                    for infected_citizen in [c for c in citizens if c.status in self.infection_stages]:
                        if any([citizen.masked, infected_citizen.masked]):
                            if random.random() < self.transmission_mask * contact_rate:
                                contact_list.append(citizen)
                        if random.random() < contact_rate:
                            contact_list.append(citizen)

        for citizen in contact_list:
            self.spread_disease(citizen)
            # Log the newly infected agents

def log_agent_symptoms_chages(old_symptoms, new_symptoms):
    removed_symptoms = []
    added_symptoms = []
    for symptom in old_symptoms:
        if symptom not in new_symptoms:
            removed_symptoms.append(symptom)

    for symptom in new_symptoms:
        if symptom not in old_symptoms:
            added_symptoms.append(symptom)

    if removed_symptoms:
        logger.debug(f'Removed Symptoms: {removed_symptoms}')
    if added_symptoms:
        logger.debug(f'Added Symptoms: {added_symptoms}')
    else:
        logger.debug(f'No Symptoms were modified')