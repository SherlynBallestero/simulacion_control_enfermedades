import argparse
from ai.genetic_algorythm import GA
import logging
from simulation.enviroment.maps import TEST_CITY_1
from simulation.enviroment.environment import Environment
from simulation.epidemic.epidemic_model import EpidemicModel
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt

def simulate(env, steps_num):
    for step in range(steps_num):
        env.step(step)
        

def fitness_func(ga_instance, solution = None, solution_idx = None):
    sim_days = 31
    sim_hours = sim_days * 24
    sim_steps = sim_hours * 6

    map = TEST_CITY_1
    epidemic_model = EpidemicModel()
    env = Environment(5, epidemic_model, map, solution)
    simulate(env, sim_steps)
    sum = 0
    a = env.dissease_step_progression[-1]
    
    for x in a:
        if x == 'susceptible':
            continue
        if x == 'recovered':
            continue
        sum += a[x]
        
    return sum

if __name__ == '__main__':
    
    # Inicializar el ArgumentParser
    parser = argparse.ArgumentParser(description="Aceptar -t.")

    # Definir el argumento opcional -t
    parser.add_argument("-t", "--train", action="store_true", help="Ejecutar en modo de entrenamiento")

    # Parsear los argumentos
    args = parser.parse_args()

    # Comprobar si el argumento -t fue proporcionado
    if args.train:
        print("Modo training activado")
        ga = GA()
        ga(fitness_func)
        
    else:
        print("Modo normal")
        ga = GA()
        ga(fitness_func)