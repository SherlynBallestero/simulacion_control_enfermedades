import pygad
import numpy as np

class GA:
    def __init__(self):
        self.elements = ['mask_use', 'social_distancing', 'tests_and_diagnosis', 'contact_tracing', 'vaccination', 'quarantine', 'isolation']

    def __call__(self, fitness_func):
        sol = {}
        solution_list = []
        # Configuración del algoritmo genético
        gene_space = [{'low': 0, 'high': 1}] * len(self.elements) 
        ga_instance = pygad.GA(num_generations=10,
                            num_parents_mating=2,
                            fitness_func=fitness_func,
                            sol_per_pop=2,
                            num_genes=len(self.elements),
                            gene_space=gene_space,
                            mutation_percent_genes=20,
                            delay_after_gen=0)

        ga_instance.run()
        solution, solution_fitness, solution_idx = ga_instance.best_solution()
        print(f"Mejor solución: {solution}, con fitness: {solution_fitness}")
        sol[solution_fitness] = solution
        solution_list = solution

        # Visualizar el fitness
        # ga_instance.plot_fitness()
        return solution_list


# int_min_val = [0, -5] # Dominios mínimos para las variables
# int_max_val = [10, 5] # Dominios máximos para las variables

# # Definir los dominios de las variables reales
# real_min_val = [0.0, -0.5] # Dominios mínimos para las variables reales
# real_max_val = [1.0, 0.5] # Dominios máximos para las variables reales

# # Definición del espacio de valores para cada gen
# gene_space = [
#     {'low': -5, 'high': 5}, # Gen 1: enteros entre -5 y 5
#     {'low': 0, 'high': 10}, # Gen 2: números flotantes entre 0 y 10
#     # Puedes agregar más genes aquí
# ]

# ga_instance = pygad.GA(num_generations =100,
#                        num_parents_mating=5,
#                        fitness_func=fitness_func,
#                        sol_per_pop=10,
#                        num_genes=len(gene_space),
#                        gene_space=gene_space,
#                     #    init_range_low=real_min_val,
#                     #    init_range_high=real_max_val,
#                        gene_type=[int, float])


