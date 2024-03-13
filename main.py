import pygame
import matplotlib.pyplot as plt
from simulation.agents import Agent
from simulation.environment import Environment
from simulation.epidemic import EpidemicModel

# Define simulation parameters
NUM_AGENTS = 100
X_LIMIT = 800
Y_LIMIT = 600
TRANSMISSION_RATE = 0.2
RECOVERY_RATE = 0.1
NUM_STEPS = 100

# Initialize environment and epidemic model
env = Environment(X_LIMIT, Y_LIMIT, NUM_AGENTS)
epidemic_model = EpidemicModel(TRANSMISSION_RATE, RECOVERY_RATE)

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((X_LIMIT, Y_LIMIT))
clock = pygame.time.Clock()

# Matplotlib initialization
plt.figure(figsize=(8, 6))

# Main simulation loop
for step in range(NUM_STEPS):
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Update agents and epidemic model
    env.step()
    epidemic_model.step(env.agents)

    # Visualize simulation using Pygame
    screen.fill((255, 255, 255))  # Clear screen
    for agent in env.agents:
        pygame.draw.circle(screen, (0, 0, 255), (int(agent.location[0]), int(agent.location[1])), 5)
    pygame.display.flip()
    clock.tick(30)  # FPS

    # Visualize simulation using Matplotlib
    plt.clf()  # Clear previous plot
    x = [agent.location[0] for agent in env.agents]
    y = [agent.location[1] for agent in env.agents]
    plt.scatter(x, y, color='blue')
    plt.xlim(0, X_LIMIT)
    plt.ylim(0, Y_LIMIT)
    plt.title(f'Step {step + 1}')
    plt.pause(0.001)  # Pause for a short time to update plot

# Close Pygame window
pygame.quit()
