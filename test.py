# import pygame
# import logging
# # import matplotlib.pyplot as plt
# from simulation.agents.agents import Agent
# from simulation.enviroment.environment import Environment
# from simulation.epidemic import EpidemicModel
# from utils.graph import Graph
# from simulation.enviroment.sim_nodes import SimNode, PublicPlace, School, Hospital, Supermarket, Park, Library, Restaurant, Gym, Bar, Cafe
# from ai.a_star.a_star import a_star

# # Define visualization parameters
# AGENT_COLOR = {
#     'susceptible': (0, 0, 255),
#     'infected': (255, 0, 0),
#     'recovered': (0, 255, 0),
# }

# # Define simulation parameters
# NUM_AGENTS = 100
# TRANSMISSION_RATE = 0.001
# RECOVERY_RATE = 0.01
# NUM_STEPS = 280

# # Crear nodos para diferentes lugares públicos
# # Crear un grafo vacío
# city_graph = Graph()

# # Reasignar ID de los nodos existentes a una matriz cuadrada de 6x6
# school_node = School(id=(0,0), capacity=1000, activity='education', opening_hours='16', location_type='indoor', health_services_access=True, ventilation_level='high', distance_to_outdoors=0, distance_to_high_risk_places=10, daily_visitor_count=500, access_restrictions=None, classrooms=20, school_hours='8:00-16:00', supervision_level='high')
# hospital_node = Hospital(id=(0,1), capacity=500, activity='healthcare', opening_hours='24/7', location_type='indoor', health_services_access=True, ventilation_level='high', distance_to_outdoors=0, distance_to_high_risk_places=0, daily_visitor_count=200, access_restrictions=None, number_of_beds=200, specialties=['general', 'cardiology', 'oncology'], number_of_staff=200)
# supermarket_node = Supermarket(id=(0,2), capacity=500, activity='shopping', opening_hours='20', location_type='indoor', health_services_access=False, ventilation_level='high', distance_to_outdoors=0, distance_to_high_risk_places=5, daily_visitor_count=1000, access_restrictions=None, number_of_sections=10, store_size=5000)
# park_node = Park(id=(1,0), capacity=500, activity='recreation', opening_hours='20', location_type='outdoor', health_services_access=False, ventilation_level='medium', distance_to_outdoors=0, distance_to_high_risk_places=10, daily_visitor_count=200, access_restrictions=None, playground_areas=5, number_of_benches=20, park_size=10000)
# library_node = Library(id=(1,1), capacity=200, activity='learning', opening_hours='18', location_type='indoor', health_services_access=False, ventilation_level='high', distance_to_outdoors=0, distance_to_high_risk_places=10, daily_visitor_count=100, access_restrictions=None, number_of_sections=5, number_of_computers=10)
# restaurant_node = Restaurant(id=(1,2), capacity=200, activity='dining', opening_hours='22', location_type='indoor', health_services_access=False, ventilation_level='medium', distance_to_outdoors=0, distance_to_high_risk_places=5, daily_visitor_count=100, access_restrictions=None, number_of_tables=10, type_of_cuisine='variety')
# gym_node = Gym(id=(2,0), capacity=500, activity='fitness', opening_hours='20', location_type='indoor', health_services_access=False, ventilation_level='high', distance_to_outdoors=0, distance_to_high_risk_places=5, daily_visitor_count=200, access_restrictions=None, number_of_equipment=20, number_of_trainers=10)
# bar_node = Bar(id=(2,1), capacity=200, activity='socializing', opening_hours='22', location_type='indoor', health_services_access=False, ventilation_level='medium', distance_to_outdoors=0, distance_to_high_risk_places=5, daily_visitor_count=100, access_restrictions=None, number_of_tables=10, type_of_music='variety', number_of_bartenders=5)
# cafe_node = Cafe(id=(2,2), capacity=150, activity='socializing', opening_hours='20', location_type='indoor', health_services_access=False, ventilation_level='medium', distance_to_outdoors=0, distance_to_high_risk_places=5, daily_visitor_count=100, access_restrictions=None, number_of_tables=20, type_of_coffee='variety')

# # Añadir nodos al grafo
# city_graph.add_node(school_node)
# city_graph.add_node(hospital_node)
# city_graph.add_node(supermarket_node)
# city_graph.add_node(park_node)
# city_graph.add_node(library_node)
# city_graph.add_node(restaurant_node)
# city_graph.add_node(gym_node)
# city_graph.add_node(bar_node)
# city_graph.add_node(cafe_node)

# # Crear aristas entre los nodos para representar las conexiones
# # Por ejemplo, conectar nodos adyacentes en la matriz
# cost_edge = 1
# for i in range(3):
#     for j in range(3):
#         if i < 2:
#             city_graph.add_edge((i, j),(i+1, j), cost_edge) # Conectar nodos en la misma columna
#         if j < 2:
#             city_graph.add_edge((i, j), (i, j+1), cost_edge) # Conectar nodos en la misma fila
       
#         cost_edge+=1
# # testing A*
# # print(city_graph.cost(1,5))

# start_node_id = (1,2)
# goal_node_id = (2,0)
# came_from, cost_so_far = a_star(city_graph, start_node_id, goal_node_id)

# # Reconstruye el camino
# current = goal_node_id
# path = []
# while current is not None:
#     path.append(current)
#     current = came_from[current]
# path = path[::-1] # Invierte el camino para obtener el orden correcto

# print("Camino:", path)



# def logger_configuration():
#     #Creating logger configuration
#     logging.basicConfig(filename="simulation.log",
#                         format='%(asctime)s %(message)s',
#                         filemode='w')
    
#     #Creating an object
#     logger = logging.getLogger()

#     #Setting the threshold of logger to DEBUG
#     logger.setLevel(logging.DEBUG)

#     return logger

# def initializing_simulation():
#     # Initialize environment and epidemic model

#     epidemic_model = EpidemicModel(TRANSMISSION_RATE, RECOVERY_RATE)
#     env = Environment( NUM_AGENTS, epidemic_model,city_graph)
    
#     return env

# def initializing_pygame():
#     # Pygame initialization
#     pygame.init()
#     screen = pygame.display.set_mode(len(city_graph.nodes),len(city_graph.nodes))
#     clock = pygame.time.Clock()

#     return screen, clock

# def simulate(env, screen = None, clock = None):
#     # Main simulation loop
#     for step in range(NUM_STEPS):
#         # Handle events
#         # for event in pygame.event.get():
#         #     if event.type == pygame.QUIT:
#         #         pygame.quit()
#         #         quit()

#         # Update agents and epidemic model
#         env.step()

#         # Visualize simulation using Pygame
#         # screen.fill((255, 255, 255))  # Clear screen
#         # for agent in env.agents:# TODO: do not print the RegentOrgAgent
#         #     pygame.draw.circle(screen, AGENT_COLOR[agent.status], (int(agent.location), int(agent.location)), 5)
#         #     print(agent.status)
#         # pygame.display.flip()
#         # clock.tick(30)  # FPS
#         infected, susceptible, removed = 0,0,0
        
#         for agent in env.agents:
#             if agent.status == 'susceptible':
#                 susceptible += 1
#             elif agent.status == 'infected':
#                 infected += 1
#             else:
#                 removed += 1
                
#         # print(infected,susceptible,removed)
#     # Close Pygame window
#     # pygame.quit()

# if __name__ == '__main__':
#     logger = logger_configuration()
#     env = initializing_simulation()
#     # screen, clock = initializing_pygame()
#     simulate(env)

from pyswip import Prolog

if __name__ == '__main__':
    prolog = Prolog()
    prolog.consult('patterns_of_behaviour.pl')
    
    prolog.asserta('capacity_place(place2, 200)')
    
    query = f"behavior_pattern(place2, FunctionName)"
    action = []
    for result in prolog.query(query):
        action.append(result['FunctionName'])
        
    
    prolog.retractall('capacity_place(_ , _)')
    
    pass

