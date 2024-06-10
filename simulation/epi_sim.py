from simulation.enviroment.environment import Environment
from simulation.enviroment.map import Terrain
from simulation.epidemic.epidemic_model import EpidemicModel
from ai.genetic_algorythm import GA

from typing import Tuple
import random
import logging
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

logger = logging.getLogger(__name__)

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
                amount_of_agents: int = 10,
                optimization_goal: str = 'minimize_infected',
                num_generations: int = 10, 
                num_parents_mating: int = 2,
                sol_per_pop: int = 2, 
                mutation_percent_genes: int = 2
                ):
        self.steps = simulation_days * 24 * 6
        self.days = simulation_days
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
        
        self.dissease_progression = None
        
        self.canelo_parameters = []
        self.optimization_goal = optimization_goal
        
        self.num_generations = num_generations
        self.num_parents_mating = num_parents_mating
        self.sol_per_pop = sol_per_pop
        self.mutation_percent_genes = mutation_percent_genes
        self.solution = [0]*8
        
        self.genetic_a = GA(self.num_generations, self.num_parents_mating, self.sol_per_pop, self.mutation_percent_genes)
    
    def fitness_func(self):
        def minimize_infected(ga_instance, solution = None, solution_idx = None):
            self.reset_sim()
            self.initialize_simulation()
            map = self.terrain
            epidemic_model = EpidemicModel()
            debug_epidemic_k(epidemic_model)
            env = Environment(self.amount_of_agents, epidemic_model, map, solution)
            self.environment = env
            self.simulate()
            budget = env.canelo.budget
            if budget < 0:
                budget = 0
                
            sum = 0
            a = self.environment.dissease_step_progression[-1]

            for x in a:
                if x == 'susceptible':
                    continue
                if x == 'dead':
                    sum += 2*a[x]
                    continue
                
                sum += a[x]
                
            self.reset_sim()
            self.initialize_simulation()
            return sum + (budget/100000)*len(env.agents)

        if self.optimization_goal == 'minimize_infected':
            return minimize_infected

    def get_stats(self):
        dissease_progression = self.environment.dissease_step_progression
        days_evolution = []
        for step, _ in enumerate(dissease_progression):
            # Check if step is the start of a day
            if step % 144 == 0:
                day = step // 144
                logger.info(f'=== Day {day} ===')
                days_evolution.append((day, dissease_progression[step]))

        return {
            "days_evolution": days_evolution
        }

    def reset_sim(self):
        self.terrain = None
        self.epidemic_model = None
        self.environment = None
        self.genetic_a = GA(self.num_generations, self.num_parents_mating, self.sol_per_pop, self.mutation_percent_genes)

    def simulate(self):
        for step in range(self.steps):
            date = self._format_day(step)
            logger.info(f'=== Date: {date} ===')
            print(f'=== Date: {date} ===')
            self.environment.step(step)
        self.dissease_progression = self.environment.dissease_step_progression
        
    def train_canelo(self):
        self.genetic_a.ga_instance = self.genetic_a(self.fitness_func())
        self.canelo_parameters = self.genetic_a
        self.solution = self.genetic_a.get_solution_list()
        return self.genetic_a.get_solution_dict()

    def initialize_simulation(self, solution = None):
        self._initialize_terrain()
        self.epidemic_model = EpidemicModel()
        self.environment = Environment(self.amount_of_agents, self.epidemic_model, self.terrain, self.solution)

    def _initialize_terrain(self):
        '''
        Initialize terrain with blocks
        '''
        self.terrain = Terrain()
        self._initialize_grid()
        self._initialize_houses()
        self._initialize_recreational()
        self._initialize_hospitals()
        self._initialize_works()

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

def debug_epidemic_k(epidemic_model):
    k = epidemic_model.disease_k
