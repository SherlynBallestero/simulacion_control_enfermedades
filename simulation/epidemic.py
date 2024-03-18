from simulation.agents import Agent

from typing import List, Tuple
import random
import logging

class EpidemicModel:
    def __init__(self, transmission_rate: float, recovery_rate: float):
        """
        Initialize the epidemic model.

        Parameters:
            transmission_rate (float): The rate at which the disease is transmitted between agents.
            recovery_rate (float): The rate at which infected agents recover from the disease.
        """
        self.transmission_rate = transmission_rate
        self.recovery_rate = recovery_rate

    def spread_disease(self, agent: Agent, other_agent: Agent):
        """
        Spread the disease from one infected agent to another susceptible agent.

        Parameters:
            agent (Agent): The infected agent.
            other_agent (Agent): The susceptible agent.
        """
        if agent.status == 'infected' and other_agent.status == 'susceptible':
            if random.random() < self.transmission_rate:
                other_agent.status = 'infected'

    def recover(self, agent: Agent):
        """
        Simulate agent's recovery from the disease.

        Parameters:
            agent (Agent): The agent to simulate recovery for.
        """
        if agent.status == 'infected':
            if random.random() < self.recovery_rate:
                agent.status = 'recovered'

    def step(self, agents: List[Tuple[Agent, List[Agent]]]):
        """
        Perform a simulation step, where disease spreads and agents recover.

        Parameters:
            agents (List[Agent]): The list of agents in the simulation.
        """
        for (agent, neighbors) in agents:
            if agent.status == 'infected':
                # Simulate disease spread to neighboring agents
                for neighbor in neighbors:
                    self.spread_disease(agent, neighbor)
                # Simulate agent's recovery
                self.recover(agent)
