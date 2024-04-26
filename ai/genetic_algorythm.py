import pygad
import numpy as np

class GA: 
    def __init__(self,num_generations, num_parents_mating, sol_per_pop, mutation_percent_genes):
        self.elements = ['mask_use', 'social_distancing', 'tests_and_diagnosis', 'contact_tracing', 'vaccination', 'quarantine', 'isolation']
        self.num_generations = num_generations
        self.num_parents_mating = num_parents_mating
        self.sol_per_pop = sol_per_pop
        self.mutation_percent_genes = mutation_percent_genes
        self.solution_dict = {}
        self.solution_list = []
        self.ga_instance = None
        
    def __call__(self, fitness_func):
        gene_space = [{'low': 0, 'high': 1}] * len(self.elements) 
        self.ga_instance = pygad.GA(num_generations=self.num_generations,
                            num_parents_mating=self.num_parents_mating,
                            fitness_func=fitness_func,
                            sol_per_pop=self.sol_per_pop,
                            num_genes=len(self.elements),
                            gene_space=gene_space,
                            mutation_percent_genes=self.mutation_percent_genes,
                            delay_after_gen=0)

        self.ga_instance.run()
        
        solution, solution_fitness, solution_idx = self.ga_instance.best_solution()
        print(f"Mejor solución: {solution}, con fitness: {solution_fitness}")
        
        for i in self.elements:
            self.solution_dict[self.elements[i]] = solution[i]
        self.solution_list = solution

        
    def get_solution_dict(self):
        return self.solution_dict
    
    def get_solution_list(self):
        return self.solution_list
    
    def get_plot_fitness(self):
        return self.ga_instance.plot_fitness()
    
    def get_plot_genes(self):
        self.ga_instance.plot_genes()
        
    
    

