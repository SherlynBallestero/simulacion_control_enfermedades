'''
For executing the simulation without the chat interface
'''
import logging
from simulation.enviroment.maps import TEST_CITY_1
from simulation.enviroment.environment import Environment
from simulation.epidemic.epidemic_model import EpidemicModel

# Create and configure logger
logging.basicConfig(filename="simulation.log",
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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