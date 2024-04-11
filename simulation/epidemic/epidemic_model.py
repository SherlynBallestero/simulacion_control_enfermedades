from simulation.agents.agents import Agent
from utils.automaton import State
from utils.graph import Graph
from pyswip import Prolog

from typing import List, Tuple
import random
import logging

class EpidemicModel:
    def __init__(self, transmission_rate: float, dissease_progression: str = './simulation/epidemic/chony_virus_progression.pl'):
        """
        Initialize the epidemic model.

        Parameters:
            transmission_rate (float): The rate at which the disease is transmitted between agents.
            recovery_rate (float): The rate at which infected agents recover from the disease.
        """
        self.dissease_k = Prolog()
        self.dissease_k.consult(dissease_progression)
        self.transmission_rate: float = transmission_rate

    def _add_agent_k(self, agent):
        self.dissease_k.assertz(f'stage({agent.unique_id}, { " asymptomatic" })')
        self.dissease_k.assertz(f'age_group({agent.unique_id}, {agent.age_group})')
        self.dissease_k.assertz(f'symptoms({agent.unique_id}, [])')

    def _query_stage(self, agent_id: int):
        stage = list(self.dissease_k.query(f'stage({agent_id}, S)'))
        return stage[0]['S'] if stage else None

    def _query_age_group(self, agent_id: int):
        return list(self.dissease_k.query(f'age_group({agent_id}, A)'))[0]['A']

    def _query_symptoms(self, agent_id: int):
        return list(self.dissease_k.query(f'symptoms({agent_id}, S)'))[0]['S']

    def _step_dissease_query(self, agent: Agent):
        next_stage = list(self.dissease_k.query(f'step({agent.unique_id}, S)'))
        current_symptoms = list(self._query_symptoms(agent.unique_id))
        try:
            return next_stage[0], current_symptoms[0]
        except:
            return None, None
        
    def step_dissease(self, agent: Agent):
        agent_stage = self._query_stage(agent.unique_id)
        current_agent_knowlege = {}

        if not agent_stage:
            self._add_agent_k(agent)
            current_agent_knowlege['stage'] = self._query_stage(agent.unique_id)
            current_agent_knowlege['age_group'] = self._query_age_group(agent.unique_id)
            current_agent_knowlege['symptoms'] = self._query_symptoms(agent.unique_id)
            return
        
        current_agent_knowlege = {
            'symptoms': self._query_symptoms(agent.unique_id),
            'age_group': self._query_age_group(agent.unique_id),
            'stage': self._query_stage(agent.unique_id)
        }

        next_stage, current_symptoms = self._step_dissease_query(agent)
        try:
            agent.status = next_stage['S']
            agent.symptoms = current_symptoms['S']
        except:
            pass

    def spread_disease(self, agent: Agent, other_agent: Agent):
        """
        Spread the disease from one infected agent to another susceptible agent.

        Parameters:
            agent (Agent): The infected agent.
            other_agent (Agent): The susceptible agent.
        """
        if other_agent.status == 'susceptible':
            if random.random() < self.transmission_rate:
                self._add_agent_k(other_agent)


    def step(self, agents: List[Tuple[Agent, List[Agent], float]]):
        """
        Perform a simulation step, where disease spreads and agents recover.

        Parameters:
            agents (List[Agent]): The list of agents in the simulation.
        """
        for (agent, neighbors, contact_rate) in agents:
            self.step_dissease(agent)
            if agent.status == 'infected':
                # Simulate disease spread to neighboring agents
                for neighbor in neighbors:
                    if random.random() < contact_rate:
                        self.spread_disease(agent, neighbor)
