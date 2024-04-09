'''
For executing the simulation without the chat interface
'''
import logging
from testing_tools.maps import TEST_CITY_1
from simulation.enviroment.environment import Environment
from simulation.epidemic import EpidemicModel
# Create and configure logger
logging.basicConfig(filename="simulation.log",
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# def initializing_simulation():
#     # Initialize environment and epidemic model
#     epidemic_model = EpidemicModel(TRANSMISSION_RATE, RECOVERY_RATE)
#     env = Environment(X_LIMIT, Y_LIMIT, NUM_AGENTS, epidemic_model)
    
#     return env

def simulate(env, steps_num):
    # Main simulation loop
    for step in range(steps_num):
        env.step()

if __name__ == '__main__':
    sim_steps = 100
    logger.info("=== Simulation Execution Started ===")
    logger.info("=== Initializing City ===")
    map = TEST_CITY_1
    logger.info("=== Initializing Epidemic Model ===")
    epidemic_model = EpidemicModel(0.5, 0.5)
    logger.info("=== Initializing Environment ===")
    env = Environment(20, epidemic_model, map)
    logger.info(f'=== Starting Simulation Loop With {sim_steps} Steps ===')
    logger.info(f'\n\tagent_num: {len(env.agents)},\n\tinfected_agents: {len([agent for agent in env.agents if agent.status == "infected"])}')
    simulate(env, sim_steps)