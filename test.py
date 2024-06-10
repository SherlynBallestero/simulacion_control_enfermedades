from simulation.epi_sim import Simulation
from pydantic import BaseModel
import logging
import matplotlib.pyplot as plt
import numpy as np
import io

def sum_infected(stage_dist):
    return sum([value for key, value in stage_dist.items() if key not in ['recovered', 'dead', 'susceptible']])


logging.basicConfig(filename="simulation.log",
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class SimulationParameters(BaseModel):
    simulation_days: int = 10
    grid_size: int = 10
    block_capacity: int = 100
    house_amount: int = 5
    house_capacity: int = 5
    hospital_amount: int = 4
    hospital_capacity: int = 50
    hospital_hours: tuple = (8, 20)
    recreational_amount: int = 4
    recreational_capacity: int = 20
    recreational_hours: tuple = (8, 20)
    works_amount: int = 4
    works_capacity: int = 10
    work_hours: tuple = (8, 20)
    amount_of_agents: int = 1

a = SimulationParameters()
simulation = Simulation(**a.model_dump())
simulation.initialize_simulation()
simulation.simulate()

#region plotting

# Generate some data for plotting

sim_stats:dict = simulation.get_stats()['days_evolution']
days = []
infected_stats = []
susceptible_stats = []
inmune_stats = []
dead_stats = []

for i, stage_dist in sim_stats:
    days.append(i)
    infected_stats.append(sum_infected(stage_dist))
    susceptible_stats.append(stage_dist['susceptible'])
    inmune_stats.append(stage_dist['recovered'])
    dead_stats.append(stage_dist['dead'])

x = days
y = infected_stats

# Create a plot
plt.figure()
plt.plot(days, infected_stats, label='Infected', color='red')
plt.plot(days, susceptible_stats, label='Susceptible', color='blue')
plt.plot(days, inmune_stats, label='Immune', color='green')
plt.plot(days, dead_stats, label='Dead', color='black')
plt.title("Epidemic Simulation")
plt.xlabel("Days")
plt.ylabel("Population")
plt.legend()
plt.grid(True)
plt.show()

# Save the plot to a BytesIO object
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)

#endregion

#region Plotting GA

simulation.genetic_a.get_plot_fitness()
simulation.genetic_a.get_plot_genes()

#endregion