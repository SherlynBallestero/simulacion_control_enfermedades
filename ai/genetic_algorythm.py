import pygad
import numpy as np

# num_generations = 100
num_parents_mating = 5

def fitness_func(ga_instance, solution, solution_idx):
        # Supongamos que queremos que la suma de los valores de los genes sea igual a 100
    if sum(solution) != 100:
        # Si la solución no cumple con la restricción, la penalizamos
        return 0 # Valor de fitness bajo
    else:
        # Si la solución cumple con la restricción, calculamos su fitness
        return sum(solution) # Ejemplo de cálculo de fitness

int_min_val = [0, -5] # Dominios mínimos para las variables
int_max_val = [10, 5] # Dominios máximos para las variables

# Definir los dominios de las variables reales
real_min_val = [0.0, -0.5] # Dominios mínimos para las variables reales
real_max_val = [1.0, 0.5] # Dominios máximos para las variables reales

# Definición del espacio de valores para cada gen
gene_space = [
    {'low': -5, 'high': 5}, # Gen 1: enteros entre -5 y 5
    {'low': 0, 'high': 10}, # Gen 2: números flotantes entre 0 y 10
    # Puedes agregar más genes aquí
]

ga_instance = pygad.GA(num_generations =100,
                       num_parents_mating=5,
                       fitness_func=fitness_func,
                       sol_per_pop=10,
                       num_genes=len(gene_space),
                       gene_space=gene_space,
                    #    init_range_low=real_min_val,
                    #    init_range_high=real_max_val,
                       gene_type=[int, float])


ga_instance.run()

solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Mejor solución encontrada: {}, con fitness: {}".format(solution, solution_fitness))
