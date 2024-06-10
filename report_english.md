
# Disease Control Simulation

Authors:
- María de Lourdes Choy
- Alejandro Yero Valdes
- Sherlyn Ballesteros Cruz

## Introduction

In today's world, the spread of diseases has become a global challenge that requires urgent attention. Stopping this spread is essential not only for protecting people's health but also for preserving social and economic stability within communities. In this work, we will explore different strategies and measures that can be implemented to prevent and control disease spread, emphasizing the need for coordinated action at the local level.

## Simulation

The simulation focuses on modeling the spread of a fictional disease in a simulated environment, using a combination of agents, internal knowledge, and disease progression rules. There are two types of agents: individuals within the simulation, characterized by location, health status, and mask usage, and an overseeing institution within the city. The simulation allows for interaction between agents and the environment, modeling complex and dynamic behaviors.

It also incorporates public health measures, such as mandatory mask usage in various locations, quarantine implementation, isolation, curfews, and promotion of social distancing. These measures are dynamically updated based on agent interactions and internal knowledge.

## Architecture

The InterRRaP (Interactive Rational Planning) architecture focuses on agent interaction within a simulated environment, providing a clear and modular structure for developing autonomous and cooperative agent systems. This architecture consists of several layers, each with specific responsibilities, working together to enable efficient and goal-directed agent actions in a dynamic environment:

- **World Interface**: Acts as an intermediary between agents and the simulated environment, facilitating their interaction. This interface not only allows agents to perceive and act upon their surroundings but also updates the environment's state in response to agent actions. It corresponds to a mental map representing the agent's terrain knowledge, which is updated with each agent's perceptions.

- **Behavior Component**: Manages reactive agent knowledge, processes environmental information, and makes decisions about specific actions the agent should take.

- **Planning Component**: Handles short-term planning, making decisions based on the agent's internal knowledge and perception of the environment. Routine behaviors are also managed in this layer.

- **Cooperative Component**: Creates cooperative plans and objectives, facilitating agent interaction, information sharing, and collective decision-making.

## Why Use InteRRaP?

The InteRRaP agent architecture is particularly well-suited for epidemic control simulations due to several fundamental reasons. It allows representing each human individual in a population as a distinct entity or agent, attributing specific traits and behaviors. This is crucial for modeling interactions between individuals, disease transmission, and disease progression within agents, providing a detailed and granular representation of epidemic dynamics. It also enables flexible and efficient implementation of interventions and behavior modifications.


## Knowledge Base

Knowledge is one of the key aspects of the agent architecture. In the implementation, a hierarchical knowledge base is used, containing three layers corresponding to each of the previously mentioned components. This allows for a formal and logical representation of the agent's knowledge.

The knowledge base includes relevant information about the agent's health status, location, mask usage, and other crucial factors for decision-making. It dynamically updates as the agent interacts with the environment and other agents. For example, if an agent moves to a new location, previously inaccessible information is incorporated into its knowledge base, enabling the agent to update its understanding of the environment and make informed decisions.

## Citizen Agents

These agents represent citizens within the simulation. Each agent has characteristics such as location, health status, and mask usage. Agents interact with the environment and each other, making decisions based on a combination of internal knowledge and environmental perception. This allows for modeling complex and dynamic behaviors, including actions like moving to different locations, working, wearing or removing masks, and more.

## Institution Agent

The institution agent plays a crucial role in the simulation, acting as a focal point for coordination and collective decision-making among agents in the simulated environment.

### Characteristics and Purpose

It is designed to function as a leader or coordinator within the simulation. Its main purpose is to make decisions based on collective information from all agents and transmit these decisions to other agents to guide their actions. This includes decisions related to implementing public health measures, such as mask usage, quarantine, and adoption of social distancing practices.

### Functioning

Its operation relies on processing and analyzing collective information from agents using an *Expert System*. It uses a customized World Interface to obtain updated information about the environment and the status of other agents. With this information, it can make informed decisions regarding measures to control disease spread.

### Communication and Coordination

One key feature is its ability to communicate and coordinate with other agents. It uses the **Cooperative Layer** to convey decisions to other agents, facilitating coordinated actions to achieve common goals.

# Environment

The environment is an abstract representation of the space in which agents move and interact. This simulated environment is essential for modeling disease dynamics and interactions among agents in an urban context. The environment is modeled using a graph. Each node represents a specific location within the simulated environment, such as a hospital, public place, workplace, block, or bus stop. Edges represent connections between these nodes, indicating possible routes that agents can take to move between different locations. Each node also calculates a base contact probability based on its capacity and the number of agents present.
Certainly! Here's the translation of the provided text:

# Modeling Disease Progression

In the simulation, the epidemic is modeled using a reactive agent with a knowledge base implemented in Prolog. This knowledge base contains rules and information about the progression of the disease in an individual.

## How the Disease Spreads

In each iteration of the simulation, contacts are calculated (when we say "contact," we specifically refer to those that contribute to disease transmission) among agents located in the same place (node). Each node has a base contact probability, and using different hygiene measures can reduce this probability of contact. If an agent comes into contact with another infected individual, the disease spreads with a certain probability.

## Disease Progression

Disease progression describes how an infected agent can transition from one stage of infection to another, from asymptomatic to terminal. This process is modeled through a set of rules that describe the conditions under which an agent can progress from one stage to another.

### Risk Factors

Several factors can increase the risk of infection and disease progression, such as the individual's age or the population density of a node. The number of agents in a node, relative to its capacity, also plays a role. While the capacity of a node does not determine the maximum number of agents it can accommodate, beyond a certain point, the probability of contact reaches its maximum.

# AI

## Pathfinding

Using the A* algorithm to find the shortest path between two points is a strategic choice in this context, especially when minimizing agent exposure to infectious diseases. Here are the arguments in favor of this strategy:

1. **Efficiency and Precision**: A* is known for its efficiency and precision in finding shorter paths. It employs a heuristic function to guide the search, allowing the algorithm to run faster than other methods like Dijkstra's without compromising accuracy. This efficiency is crucial in environments where a rapid response is needed, such as agent mobility during an epidemic.

2. **Adaptability to Complex Environments**: A* can adapt to complex environments, including infected nodes or those with many agents, where spatial topology and movement constraints matter. This adaptability is particularly relevant in the context of epidemic control simulations, where agents must navigate environments that may include high-risk infection areas.

3. **Minimizing Disease Exposure**: Although A* is primarily used for finding the shortest path, its efficiency and precision can be tailored to minimize exposure to infectious diseases. For example, algorithm parameters can be adjusted to prioritize paths that minimize exposure to high-risk infection areas, such as rooms with infected patients. This adjustment involves considering not only the distance to the target but also the probability of disease exposure in different parts of the environment.

4. **Flexibility to Adapt to Changes**: A* is a flexible algorithm that can adjust to changes in the environment or epidemic conditions. If disease spread patterns change or new control strategies are implemented, the algorithm can be readjusted to reflect these changes.

## Natural Language User Interface and Processing

To enhance interaction with the simulation, a user interface is developed that allows users to interact with the simulation using natural language commands. Natural Language Processing (NLP) techniques are employed to interpret user commands and map them to actions within the simulation.

The Streamlit library is used to create an interactive web application called "EpiDoc," which simulates epidemic behavior. Here's a summary of its key features:

- Various functions are defined to perform different tasks, such as initializing simulation parameters, clearing simulation parameters, restarting the simulation, starting the simulation, retrieving the simulation state, obtaining statistics, generating graphs, and more.

- Informative texts are provided to guide users in using the application.

- Functions are defined to process and analyze user queries, as well as to extract specific parameters from those queries.

- The user interface of the application is created using Streamlit. The application includes a sidebar with a help button, tabs for the home, graphs, and results sections, a text input field for users to describe the epidemic simulation, and buttons to start the simulation and display results.

- When the user presses the "Start Simulation" button, their query is sent to the language model, the response is processed to obtain simulation parameters, the simulation is initialized, and the results are displayed in the corresponding tabs².


### Expert System

An expert system is a computer program that simulates human reasoning to solve a specific problem. It aims to mimic the decision-making process of an expert in a specialized field. Here are some key points about expert systems:

- **Definition**: Expert systems are applications of artificial intelligence (AI) that simulate human reasoning. They use knowledge representation, inference engines, and rule-based systems to provide expert-level advice or solutions.

- **Functionality**: Expert systems evaluate input data based on predefined rules and knowledge. They make decisions, provide recommendations, or solve problems within a specific domain.

- **Rules and Logic**: Expert systems rely on a set of rules that establish conditions and corresponding actions. For instance:
  ```
  If the infection rate is high and hospital capacity is low, implement a quarantine.
  ```

- **Evaluation**: The expert system evaluates these rules based on the current state of the simulation and previous decisions made. It generates recommendations for the institutional agent.

- **Genetic Algorithm Optimization**: To create this expert system, we use the PyGAD genetic algorithm library in Python. PyGAD optimizes a wide range of problems using genetic algorithm techniques.

- **PyGAD Overview**: PyGAD is designed to find optimal solutions by evolving a population of potential solutions over multiple generations. It uses genetic operators such as selection, crossover, and mutation to improve the fitness of individuals.

- **Application to Epidemic Control**: In a simulation focused on minimizing the number of infected agents, PyGAD can fine-tune parameters used by the institutional agent. By iteratively adjusting these parameters, the expert system aims to make informed decisions and optimize epidemic control strategies.

### How PyGAD Works

1. **Fitness Function Definition**: PyGAD requires defining a fitness function that evaluates the quality of a given solution. In the context of this simulation, the fitness function calculates the number of infected agents in a given simulation, with the goal of minimizing this number.

2. **Population Initialization**: PyGAD generates an initial population of solutions (agents) with random values within a defined range. Each solution represents a set of parameters or strategies that could be used in the epidemic control simulation.

3. **Parent Selection**: From the initial population, PyGAD selects solutions for reproduction based on their fitness. Solutions with better fitness are more likely to be chosen.

4. **Crossover and Mutation**: The selected solutions undergo crossover to generate new solutions by combining parts of the parent solutions. Subsequently, mutation is applied to introduce variations and explore new areas of the solution space.

5. **Evaluation of the New Population**: The new solutions are evaluated using the defined fitness function, and the best solutions are selected to form the new population.

6. **Iteration**: This process of selection, crossover, mutation, and evaluation is repeated for a defined number of generations, allowing the population to evolve toward higher fitness solutions.

### Why PyGAD Is Ideal for Epidemic Control Simulations

- **Flexibility**: PyGAD is highly flexible and can optimize a wide range of problems, making it suitable for epidemic control simulations that may require optimizing multiple parameters or strategies.

- **Handling Complexity**: PyGAD's ability to explore the solution space through mutation and crossover allows it to handle the inherent complexity of epidemic control systems, where interactions among multiple factors can impact disease spread.

- **Adaptability**: PyGAD can adapt to changes in the epidemic environment or control policies by reevaluating the fitness function and evolving the population toward more effective solutions.

- **Efficiency**: Through fitness-based parent selection, PyGAD can quickly converge toward optimal solutions, critical in an epidemic context where time is a crucial factor.

# Experimental Results

### For 20 agents over a 10-day range, these were the results.

| Day | Susceptible | Asymptomatic | Symptomatic | Critical | Terminal | Deceased | Recovered |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 12 | 7 | 0 | 0 | 0 | 0 | 1 |
| 1 | 1 | 0 | 2 | 1 | 0 | 3 | 13 |
| 2 | 1 | 0 | 0 | 0 | 0 | 4 | 15 |
| 3 | 1 | 0 | 0 | 0 | 0 | 4 | 15 |
| 4 | 1 | 0 | 0 | 0 | 0 | 4 | 15 |
| 5 | 1 | 0 | 0 | 0 | 0 | 4 | 15 |
| 6 | 1 | 0 | 0 | 0 | 0 | 4 | 15 |
| 7 | 1 | 0 | 0 | 0 | 0 | 4 | 15 |
| 8 | 1 | 0 | 0 | 0 | 0 | 4 | 15 |
| 9 | 1 | 0 | 0 | 0 | 0 | 4 | 15 |
| 10 | 1 | 0 | 0 | 0 | 0 | 4 | 15 |

### For 50 agents over a 10-day range, these were the results:

| Day | Susceptible | Asymptomatic | Symptomatic | Critical | Terminal | Deceased | Recovered |
|-----|-------------|--------------|-------------|---------|----------|-------|------------|
| 0   | 35          | 4            | 1           | 0       | 0        | 0     | 10         |
| 1   | 19          | 1            | 3           | 1       | 1        | 1     | 24         |
| 2   | 13          | 0            | 1           | 0       | 1        | 4     | 31         |
| 3   | 12          | 0            | 1           | 0       | 0        | 5     | 32         |
| 4   | 8           | 0            | 1           | 2       | 0        | 5     | 34         |
| 5   | 8           | 0            | 0           | 1       | 0        | 6     | 35         |
| 6   | 8           | 0            | 0           | 0       | 0        | 7     | 35         |
| 7   | 8           | 0            | 0           | 0       | 0        | 7     | 35         |
| 8   | 8           | 0            | 0           | 0       | 0        | 7     | 35         |
| 9   | 8           | 0            | 0           | 0       | 0        | 7     | 35         |
| 10 | 8           | 0            | 0           | 0       | 0        | 7     | 35         |

### For 100 agents over a 15-day range, these were the results:

| Day | Susceptible | Asymptomatic | Symptomatic | Critical | Terminal | Deceased | Recovered |
|-----|-------------|--------------|-------------|---------|----------|-------|------------|
| 0   | 87          | 8            | 2           | 0       | 0        | 0     | 3          |
| 1   | 10          | 1            | 4           | 0       | 2        | 1     | 82         |
| 2   | 4           | 0            | 2           | 3       | 1        | 5     | 85         |
| 3   | 2           | 0            | 1           | 1       | 0        | 8     | 88         |
| 4   | 2           | 0            | 0           | 1       | 0        | 9     | 88         |
| 5   | 2           | 0            | 0           | 0       | 0        | 10    | 88         |
| 6   | 2           | 0            | 0           | 0       | 0        | 10    | 88         |
| 7   | 2           | 0            | 0           | 0       | 0        | 10    | 88         |
| 8   | 2           | 0            | 0           | 0       | 0        | 10    | 88         |
| 9   | 2           | 0            | 0           | 0       | 0        | 10    | 88         |
| 10 | 2           | 0            | 0           | 0       | 0        | 10    | 88         |
| 11 | 2           | 0            | 0           | 0       | 0        | 10    | 88         |
| 12 | 2           | 0            | 0           | 0       | 0        | 10    | 88         |
| 13 | 2           | 0            | 0           | 0       | 0        | 10    | 88         |
| 14 | 2           | 0            | 0           | 0       | 0        | 10    | 88         |
| 15 | 2           | 0            | 0           | 0       | 0        | 10    | 88         |

### For 200 agents over a 15-day range, these were the results:

| Day | Susceptible | Asymptomatic | Symptomatic | Critical | Terminal | Deceased | Recovered |
|-----|-------------|--------------|-------------|---------|----------|-------|------------|
| 0   | 156         | 29           | 4           | 0       | 0        | 0     | 11         |
| 1   | 0           | 2            | 11          | 3       | 2        | 11    | 171        |
| 2   | 0           | 1            | 3           | 2       | 0        | 17    | 177        |
| 3   | 0           | 1            | 3           | 0       | 1        | 17    | 178        |
| 4   | 0           | 0            | 0           | 2       | 0        | 18    | 180        |
| 5   | 0           | 0            | 0           | 1       | 1        | 18    | 180        |
| 6   | 0           | 0            | 1           | 0       | 0        | 19    | 180        |
| 7   | 0           | 0            | 1           | 0       | 0        | 19    | 180        |
| 8   | 0           | 0            | 0           | 1       | 0        | 19    | 180        |
| 9   | 0           | 0            | 0           | 1       | 0        | 19    | 180        |
| 10 | 0           | 0            | 0           | 0       | 0        | 20    | 180        |
| 11 | 0           | 0            | 0           | 0       | 0        | 20    | 180        |
| 12 | 0           | 0            | 0           | 0       | 0        | 20    | 180        |
| 13 | 0           | 0            | 0           | 0       | 0        | 20    | 180        |
| 14 | 0           | 0            | 0           | 0       | 0        | 20    | 180        |

### For 250 agents over a 15-day range, these were the results:

| Day | Susceptible | Asymptomatic | Symptomatic | Critical | Terminal | Deceased | Recovered |
|-----|-------------|--------------|-------------|---------|----------|-------|------------|
| 0   | 221         | 10           | 3           | 0       | 0        | 0     | 16         |
| 1   | 0           | 0            | 9           | 1       | 0        | 13    | 227        |
| 2   | 0           | 0            | 5           | 2       | 0        | 14    | 229        |
| 3   | 0           | 0            | 0           | 1       | 1        | 15    | 233        |
| 4   | 0           | 0            | 0           | 2       | 0        | 15    | 233        |
| 5   | 0           | 0            | 0           | 1       | 0        | 16    | 233        |
| 6   | 0           | 0            | 1           | 0       | 0        | 16    | 233        |
| 7   | 0           | 0            | 0           | 0       | 0        | 16    | 234        |
| 8   | 0           | 0            | 0           | 0       | 0        | 16    | 234        |
| 9   | 0           | 0            | 0           | 0       | 0        | 16    | 234        |
| 10 | 0           | 0            | 0           | 0       | 0        | 16    | 234        |
| 11 | 0           | 0            | 0           | 0       | 0        | 16    | 234        |
| 12 | 0           | 0            | 0           | 0       |

The experimental results presented in the simulation reveal several patterns and trends that are relevant for understanding the dynamics of disease spread in different contexts and populations. Here's an interpretation based on these data:

1. **Scalability and Effectiveness of Interventions**: As the number of agents increases, there is a general trend toward greater effectiveness of interventions in reducing disease spread. This suggests that epidemic control strategies may be more effective in larger populations, which is crucial for managing disease outbreaks in real-world scenarios.

2. **Impact of Disease Initialization**: The results show that the initial number of infected agents (symptomatic or asymptomatic) significantly impacts the epidemic's evolution. In cases with fewer agents (20 and 50), the initial impact is more pronounced, while in cases with more agents (100, 150, 200, 250), the epidemic appears to reach a steady state more quickly, possibly due to the population's greater capacity to transmit the disease.

3. **Epidemic Duration**: The epidemic's duration seems to be influenced by the number of agents and intervention effectiveness. This particular epidemic has a short duration due to its lethality, reaching a steady state rapidly.

4. **Recovery and Mortality**: As the number of agents increases, the proportion of recovered agents and the mortality rate appear to decrease. This could indicate that interventions are more effective in larger populations, allowing for faster recovery and lower mortality rates.

# Conclusions

The experimental results provide valuable insights into how epidemic control interventions can impact disease spread and management in different contexts. However, it's essential to remember that these results are specific to the simulation and may not fully reflect the complexity and variability of real-world epidemics. Adapting epidemic control strategies must consider various factors, including disease dynamics, population characteristics, and healthcare system response capabilities.

# Recommendations and Future Changes

It is recommended to conduct a more in-depth study of Prolog to better understand the workings of this programming language. Originally, Prolog was used for the agents' knowledge base; however, due to its limited memory capacity, a knowledge base implemented in Python was chosen instead. Nevertheless, Prolog was retained for simulating the spread of the epidemic. It's essential to note that there are limitations regarding the number of agents that can be handled, as the limit cannot exceed 300 agents.

# Bibliography

[1] https://towardsdatascience.com/introducing-geneal-a-genetic-algorithm-python-library-db69abfc212c  
[2] https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009149  
[3] https://github.com/diogomatoschaves/geneal  
[4] https://jmvidal.cse.sc.edu/library/muller93a.pdf





