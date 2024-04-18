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
        logger.info(f'=== Step: {step} ===')
        logger.info(f'Starting cond:\n\tagent_num: {len(env.agents)},\n\tinfected_agents: {len([agent for agent in env.agents if agent.status == "infected"])}')
        env.step(step)
        logger.info(f'Ending cond:\n\tagent_num: {len(env.agents)},\n\tinfected_agents: {len([agent for agent in env.agents if agent.status == "infected"])}')

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
    env = Environment(20, epidemic_model, map)
    logger.info(f'=== Starting Simulation Loop With {sim_steps} Steps ===')
    simulate(env, sim_steps)