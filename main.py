import pygame
import logging
import matplotlib.pyplot as plt
from simulation.agents.agents import Agent
from simulation.enviroment.environment import Environment
from simulation.epidemic import EpidemicModel


# Define visualization parameters
AGENT_COLOR = {
    'susceptible': (0, 0, 255),
    'infected': (255, 0, 0),
    'recovered': (0, 255, 0),
}

# Define simulation parameters
NUM_AGENTS = 100
X_LIMIT = 800
Y_LIMIT = 600
TRANSMISSION_RATE = 0.4
RECOVERY_RATE = 0.01
NUM_STEPS = 280


def logger_configuration():
    #Creating logger configuration
    logging.basicConfig(filename="simulation.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    
    #Creating an object
    logger = logging.getLogger()

    #Setting the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)

    return logger

def initializing_simulation():
    # Initialize environment and epidemic model
    epidemic_model = EpidemicModel(TRANSMISSION_RATE, RECOVERY_RATE)
    env = Environment(X_LIMIT, Y_LIMIT, NUM_AGENTS, epidemic_model)
    
    return env

def initializing_pygame():
    # Pygame initialization
    pygame.init()
    screen = pygame.display.set_mode((X_LIMIT, Y_LIMIT))
    clock = pygame.time.Clock()

    return screen, clock

def simulate(env, screen, clock):
    # Main simulation loop
    for step in range(NUM_STEPS):
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Update agents and epidemic model
        env.step()

        # Visualize simulation using Pygame
        screen.fill((255, 255, 255))  # Clear screen
        for agent in env.agents:# TODO: do not print the RegentOrgAgent
            pygame.draw.circle(screen, AGENT_COLOR[agent.status], (int(agent.location[0]), int(agent.location[1])), 5)
            print(agent.status)
        pygame.display.flip()
        clock.tick(30)  # FPS

    # Close Pygame window
    pygame.quit()

if __name__ == '__main__':
    logger = logger_configuration()
    env = initializing_simulation()
    screen, clock = initializing_pygame()
    simulate(env, screen, clock)
