'''
For executing the simulation without the chat interface
'''
import logging
from simulation.enviroment.maps import TEST_CITY_1
from simulation.enviroment.environment import Environment
from simulation.epidemic.epidemic_model import EpidemicModel
import matplotlib.pyplot as plt

# Create and configure logger
logging.basicConfig(filename="simulation.log",
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def plot_dissease_evolution_days(dissease_progression, days):
    '''
    Shows a bar plot of the disease evolution in the population, the x-axis represents the different states of the disease, the y-axis the number of agents, the bar has different colors depending of the state of the disease
    '''
    # Data for plotting
    states = ['susceptible', 'asymptomatic', 'symptomatic', 'critical', 'terminal', 'dead', 'recovered']
    colors = ['y', 'g', 'r', 'c', 'm', 'b', 'k']
    x = range(days) + 1
    y = [[day[state] for day in dissease_progression] for state in states]
    addition = [0] * len(y[0])
    for i, data in enumerate(y):
        plt.bar(x, data, color=colors[i], bottom=addition)
        addition = [sum(x) for x in zip(addition, data)]

    # Plotting
    plt.show()


def simulate(env, steps_num):
    # Main simulation loop
    for step in range(steps_num):
        date = format_day(step)
        logger.info(f'=== Step: {date} ===')
        # log_infection_status(env, 'Starting cond:')
        env.step(step)
        # log_infection_status(env, 'Ending cond:')

def log_infection_status(env, msg):
    total_agents = len(env.agents)
    healthy_agents = len([healthy_agent for healthy_agent in env.agents if healthy_agent.status if healthy_agent.status == 'susceptible'])
    infected_agents = len([infected_agent for infected_agent in env.agents if infected_agent.status if infected_agent.status == 'asymptomatic'])
    symptomatic_agents = len([symptomatic_agent for symptomatic_agent in env.agents if symptomatic_agent.status if symptomatic_agent.status == 'symptomatic'])
    critical_agents = len([critical_agent for critical_agent in env.agents if critical_agent.status if critical_agent.status == 'critical'])
    terminal_agents = len([terminal_agent for terminal_agent in env.agents if terminal_agent.status if terminal_agent.status == 'terminal'])
    dead_agents = len([dead_agent for dead_agent in env.agents if dead_agent.status if dead_agent.status == 'dead'])
    recovered_agents = len([recovered_agent for recovered_agent in env.agents if recovered_agent.status if recovered_agent.status == 'recovered'])
    logger.info(f'{msg}\n\tagent_num: {total_agents}\n\thealthy_agents: {healthy_agents}\n\tinfected_agents: {infected_agents}\n\tsymptomatic_agents: {symptomatic_agents}\n\tcritical_agents: {critical_agents}\n\tterminal_agents: {terminal_agents}\n\tdead_agents: {dead_agents}\n\trecovered_agents: {recovered_agents}\n\t')

def format_day(step_num):
    # Calculating day of the week, hour and min sim_days = 31 sim_hours = sim_days * 24 sim_steps = sim_hours * 6
    days_of_the_week = [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday"]
    min = step_num % 6 * 10
    hour = step_num // 6 % 24
    day = step_num // 6 // 24 % 7
    week_day = days_of_the_week[day]
    month_day = step_num // 6 // 24
    return week_day, month_day, hour, min


# For testing
d_evol = [
    {
        'susceptible':4,
        'asymptomatic':0,
        'symptomatic':0,
        'critical':0,
        'terminal':0,
        'dead':0,
        'recovered':0
    },
    {
        'susceptible':3,
        'asymptomatic':1,
        'symptomatic':0,
        'critical':0,
        'terminal':0,
        'dead':0,
        'recovered':0
    },
    {
        'susceptible':2,
        'asymptomatic':1,
        'symptomatic':1,
        'critical':0,
        'terminal':0,
        'dead':0,
        'recovered':0
    },
    {
        'susceptible':1,
        'asymptomatic':1,
        'symptomatic':1,
        'critical':1,
        'terminal':0,
        'dead':0,
        'recovered':0
    }
]


if __name__ == '__main__':
    sim_days = 31
    sim_hours = sim_days * 24
    sim_steps = sim_hours * 6

    logger.info("=== Simulation Execution Started ===")
    logger.debug("=== Initializing City ===")
    map = TEST_CITY_1
    logger.debug("=== Initializing Epidemic Model ===")
    epidemic_model = EpidemicModel()
    logger.debug("=== Initializing Environment ===")
    env = Environment(4, epidemic_model, map)
    logger.info(f'=== Starting Simulation Loop With {sim_steps} Steps ===')
    simulate(env, sim_steps)
    plot_dissease_evolution_days(env.dissease_evolution, len(env.dissease_evolution))
    # plot_dissease_evolution_days(d_evol, len(d_evol))
    pass