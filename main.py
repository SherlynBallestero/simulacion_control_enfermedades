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
        print(date)
        logger.info(f'=== Step: {date} ===')
        logger.info(f'Starting cond:\n\tagent_num: {len(env.agents)},\n\tinfected_agents: {len([agent for agent in env.agents if agent.status == "infected"])}')
        env.step(step)
        logger.info(f'Ending cond:\n\tagent_num: {len(env.agents)},\n\tinfected_agents: {len([agent for agent in env.agents if agent.status == "infected"])}')

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
    env = Environment(1, epidemic_model, map)
    logger.info(f'=== Starting Simulation Loop With {sim_steps} Steps ===')
    simulate(env, sim_steps)