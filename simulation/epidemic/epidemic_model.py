from simulation.agents.agents import Agent
from utils.automaton import State
from utils.graph import Graph
from pyswip import Prolog

from typing import List, Tuple
import random
import logging
import itertools

class EpidemicModel:
    def __init__(self, dissease_description: str = './simulation/epidemic/chony_virus_progression.pl'):
        """
        Initialize the epidemic model.

        Parameters:
            transmission_rate (float): The rate at which the disease is transmitted between agents.
            recovery_rate (float): The rate at which infected agents recover from the disease.
        """
        self.dissease_k = Prolog()
        self.dissease_k.consult(dissease_description)
        self.transmission_rate: float = self.dissease_k.query('base_transmission_rate(R)')[0]['R']
        self.infection_stages: List[str] = self.dissease_k.query('infection_stages(Stages)')[0]['Stages']
        self.mask_effectiveness: float = self.dissease_k.query('mask_effectiveness(E)')[0]['E']
        self.transmission_mask: float = self.transmission_rate * self.mask_effectiveness

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
        return next_stage, current_symptoms
    
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
        agent.status = next_stage['S']
        agent.symptoms = current_symptoms['S']        


    def _infect_citizen(self, agent: Agent):
        """
        Infect an agent with the disease.
        """
        self.dissease_k.assertz(f'stage({agent.unique_id}, { " asymptomatic" })')
        self.dissease_k.assertz(f'age_group({agent.unique_id}, {agent.age_group})')
        self.dissease_k.assertz(f'symptoms({agent.unique_id}, [])')
        self.dissease_k.assertz(f'vaccinated({agent.unique_id}, {agent.vaccinated})')

    def spread_disease(self, agent: Agent):
        """
        Spread the disease from one infected agent to another susceptible agent.

        Parameters:
            agent (Agent): The infected agent.
            other_agent (Agent): The susceptible agent.
        """
        if random.random() < self.transmission_rate:
            self._infect_citizen(agent)

    def step(self, nodes: List[Tuple[List[Agent], float]]):
        """
        Perform a simulation step, where disease spreads and agents recover.

        Parameters:
            agents (List[Agent]): The list of agents in the simulation.
        """

        contact_list = []
        for (citizens, contact_rate) in nodes:
            for citizen in citizens:
                # Calculating dissease for infected citizens
                if citizen.status in self.infection_stages:
                    self.step_dissease(citizen)
                # Getting healthy peopple who contacted infected citizens
                else:
                    for infected_citizen in [c for c in citizens if c.status in self.infection_stages]:
                        if any([citizen.masked, infected_citizen.masked]):
                            if random.random() < self.transmission_mask * contact_rate:
                                contact_list.append(citizen)
                        if random.random() < contact_rate:
                            contact_list.append(citizen)

        # Calculating dissease for healthy citizens who contacted infected citizens
        for citizen in contact_list:
            self.spread_disease(citizen)