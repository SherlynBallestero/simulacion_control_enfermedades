from simulation.enviroment.environment import Environment
from simulation.enviroment.map import Terrain
from simulation.epidemic.epidemic_model import EpidemicModel

from typing import Tuple
import random
import logging
import matplotlib.pyplot as plt

logging.basicConfig(filename="simulation.log",
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class Simulation:
    def __init__(self,
                simulation_days: int = 31,
                grid_size: int = 10,
                block_capacity: int = 100,
                house_amount: int = 10,
                house_capacity: int = 5,
                hospital_amount: int = 4,
                hospital_capacity: int = 50,
                hospital_hours: Tuple = (8, 20),
                recreational_amount: int = 4,
                recreational_capacity: int = 20,
                recreational_hours: Tuple = (8, 20),
                works_amount: int = 4,
                works_capacity: int = 10,
                work_hours: Tuple = (8, 20),
                amount_of_agents: int = 10
                ):
        self.steps = simulation_days * 24 * 6
        self.terrain: Terrain = None
        self.epidemic_model: EpidemicModel = None
        self.environment: Environment = None

        self.amount_of_agents = amount_of_agents
        
        self.grid_size = grid_size
        self.block_capacity = block_capacity
        
        self.house_amount = house_amount
        self.house_capacity = house_capacity

        self.hospital_amount = hospital_amount
        self.hospital_capacity = hospital_capacity
        self.hospital_opening_hours, self.hospital_closing_hours = hospital_hours

        self.recreational_amount = recreational_amount
        self.recreational_capacity = recreational_capacity
        self.recreational_opening_hours, self.recreational_closing_hours = recreational_hours

        self.works_amount = works_amount
        self.works_capacity = works_capacity
        self.work_opening_hours, self.work_closing_hours = work_hours

    def reset_sim(self):
        self.terrain = None
        self.epidemic_model = None
        self.environment = None

    def simulate(self):
        self.initialize_simulation()
        for step in range(self.steps):
            date = self.format_day(step)
            print(f'=== Step: {date} ===')
            self.environment.step(step)

    def initialize_simulation(self):
        self._initialize_terrain()
        self.epidemic_model = EpidemicModel()
        self.environment = Environment(self.amount_of_agents, self.epidemic_model, self.terrain)
        #TODO: Initialize the Canelo Agent from this class

    def _initialize_terrain(self):
        '''
        Initialize terrain with blocks
        '''
        self.terrain = Terrain()
        self._initialize_grid()
        self._initialize_houses()
        self._initialize_recreational()
        self._initialize_hospitals()

    def _initialize_grid(self):
        '''
        Initialize grid with nodes
        '''
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                self.terrain.add_block((x, y), self.block_capacity)
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if i < self.grid_size - 1:
                    node1 = self.terrain[(i,j)]
                    node2 = self.terrain[(i+1, j)]
                    self.terrain.add_edge(node1[0].id, node2[0].id)
                if j < self.grid_size - 1:
                    node1 = self.terrain[(i,j)]
                    node2 = self.terrain[(i, j+1)]
                    self.terrain.add_edge(node1[0].id, node2[0].id)

    def _initialize_houses(self):
        '''
        Initialize houses in the grid
        '''
        for _ in range(self.house_amount):
            house_addr = random.choice(list(self.terrain.nodes_by_addrs.keys()))
            self.terrain.add_house(house_addr, self.house_capacity)

    def _initialize_recreational(self):
        '''
        Initialize recreational places in the grid
        '''
        for _ in range(self.recreational_amount):
            recreational_addr = random.choice(list(self.terrain.nodes_by_addrs.keys()))
            self.terrain.add_recreational(recreational_addr, self.recreational_capacity, self.recreational_opening_hours, self.recreational_closing_hours)

    def _initialize_hospitals(self):
        '''
        Initialize hospitals in the grid
        '''
        for _ in range(self.hospital_amount):
            hospital_addr = random.choice(list(self.terrain.nodes_by_addrs.keys()))
            self.terrain.add_hospital(hospital_addr, self.hospital_capacity, self.hospital_opening_hours, self.hospital_closing_hours)

    def _initialize_works(self):
        '''
        Initialize workspaces in the grid
        '''
        for _ in range(self.works_amount):
            work_addr = random.choice(list(self.terrain.nodes_by_addrs.keys()))
            self.terrain.add_work(work_addr, self.works_capacity, self.work_opening_hours, self.work_closing_hours)

    def _format_day(self, step_num):
        '''
        Calculating day of the week, hour and min from step number
        '''
        days_of_the_week = [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday"]
        min = step_num % 6 * 10
        hour = step_num // 6 % 24
        day = step_num // 6 // 24 % 7
        week_day = days_of_the_week[day]
        month_day = step_num // 6 // 24
        
        return week_day, month_day, hour, min

    def sirr_plot(self, start_day: int = 0, end_day: int = None):
        '''
        Returns the  susceptible-infected-recovered-dead plot to show in the streamlit app 
        '''
        if end_day is None:
            end_day = self.steps // 6 // 24
        x = range(end_day - start_day)
        y = [[self.environment.dissease_step_progression[day * 6 * 24][state] for day in range(end_day)] for state in self.environment.states]
        addition = [0] * len(y[0])
        for i, data in enumerate(y):
            plt.bar(x, data, color=self.environment.colors[i], bottom=addition)
            addition = [sum(x) for x in zip(addition, data)]
        plt.show()#TODO: change this so its showed in streamlit

    def dissease_progression_plot(self, start_day: int = 0, end_day: int = None):
        '''
        Returns the dissease progression plot to show in the streamlit app 
        '''
        if end_day is None:
            end_day = self.steps // 6 // 24
        x = range(end_day - start_day)
        y = [[self.environment.dissease_step_progression[day * 6 * 24][state] for day in range(end_day)] for state in self.environment.states]
        addition = [0] * len(y[0])
        for i, data in enumerate(y):
            plt.bar(x, data, color=self.environment.colors[i], bottom=addition)
            addition = [sum(x) for x in zip(addition, data)]
        plt.show()#TODO: change this so its showed in streamlit

