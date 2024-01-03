import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random







def evaluate_path(path, precedence_matrix):
    num_tasks = len(path)
    
    # Vérifier les contraintes de précédence pour chaque paire d'opérations
    for i in range(num_tasks):
        for j in range(i+1, num_tasks):
            task_i = path[i]
            task_j = path[j]
            
            # Vérifier si l'opération j peut être effectuée avant l'opération k
            if precedence_matrix[task_j][task_i] == 1:
                return False  # Contrainte de précédence violée
    
    # Vérifier si une tâche apparaît deux fois dans le chemin
    if len(set(path)) != len(path):
        return False  # Contrainte de duplication de tâche violée
    
    return True
# evaluation of time 
def evaluate_fitness(path, execution_time):
    total_time = 0
    current_task = 0
    for next_task in path:
        total_time += execution_time[current_task][next_task]
        current_task = next_task
    return total_time




def generate_initial_population(num_population, num_tasks):
    population = []
    for _ in range(num_population):
        path = random.sample(range(num_tasks), num_tasks)
        if path not in population:
            population.append(path)
    return population

def select_parents(population, num_parents):
    parents = random.sample(population, num_parents)
    return parents

def crossover(parents):
    # Point de croisement
    crossover_point = random.randint(1, len(parents[0])-1)
    
    # Générer les enfants par croisement
    child1 = parents[0][:crossover_point] + parents[1][crossover_point:]
    child2 = parents[1][:crossover_point] + parents[0][crossover_point:]
    
    return child1, child2

def mutate(path):
    # Choisir deux positions aléatoires à échanger
    idx1, idx2 = random.sample(range(len(path)), 2)
    
    # Effectuer la mutation
    path[idx1], path[idx2] = path[idx2], path[idx1]
    
    return path

def genetic_algorithm(num_tasks, num_population, num_generations, precedence_matrix,execution_time):
    # Génération initiale de la population
    population = generate_initial_population(num_population, num_tasks)
    
    for _ in range(num_generations):
        # Sélection des parents
        parents = select_parents(population, 2)
        
        # Croisement pour obtenir les enfants
        child1, child2 = crossover(parents)
        
        # Mutation des enfants
        mutated_child1 = mutate(child1)
        mutated_child2 = mutate(child2)
        
        # Évaluation des enfants mutés
        if evaluate_path(mutated_child1, precedence_matrix):
            population.append(mutated_child1)
        if evaluate_path(mutated_child2, precedence_matrix):
            population.append(mutated_child2)
        
        # Sélection des meilleurs individus pour la génération suivante
        population = sorted(population, key=lambda x: evaluate_path(x, precedence_matrix), reverse=True)[:num_population]
    

    list_best_paths=[]
    for path in population:
        if (evaluate_path(path, precedence_matrix)) and (path[0] == entry_task) and (path not in list_best_paths):
            list_best_paths.append(path)
    

    min_temps=evaluate_fitness(list_best_paths[0],execution_time)
    best_path=list_best_paths[0]
    for path in list_best_paths[1:]:
        if evaluate_fitness(path,execution_time)<=min_temps:
            best_path=path
            min_temps=evaluate_fitness(path,execution_time)
    print("Temps du chein optimal :",evaluate_fitness(best_path,execution_time))
    return best_path
            
    














# Exemple d'utilisation
tasks = [0, 1, 2, 3, 4, 5]  # Remplacez par vos tâches réelles

entry_task = 0  # Tâche d'entrée obligatoire
precedence_matrix = np.array([[0, 1, 1, 1, 0, 0],
                              [0, 0, 0, 0, 1, 0],
                              [0, 0, 0, 0, 1, 0],
                              [0, 0, 0, 0, 1, 0],
                              [0, 0, 0, 0, 0, 1],
                              [0, 0, 0, 0, 0, 0]])  # Remplacez par votre matrice de précédence réelle

execution_time =    np.array([[0, 5.62, 0.925, 0.5, 0, 0],
                              [0, 0, 0.943, 0.502, 0.505, 0],
                              [0, 5.645, 0, 0.51, 0.515, 0],
                              [0, 5.61, 0.925, 0, 0.502, 0],
                              [0, 0, 0, 0, 0, 0.505],
                              [0, 0, 0, 0, 0, 0]])  # Remplacez par votre matrice de précédence réelle


execution_time2 =    np.array([[0, 8, 2, 1, 0, 0],
                              [0, 0, 0.5, 1, 1.2, 0],
                              [0, 7.4, 0, 2, 2.2, 0],
                              [0, 7.8, 2, 0, 1.4, 0],
                              [0, 0, 0, 0, 0, 2],
                              [0, 0, 0, 0, 0, 0]])  # Remplacez par votre matrice de précédence réelle

execution_time3 =    np.array([[0, 0.62, 1.256, 7.79, 0, 0],
                              [0, 0, 0.83, 2.3, 6.3, 0],
                              [0, 5.2, 0, 11.2, 0.69, 0],
                              [0, 1.3, 8.7, 0, 9.6, 0],
                              [0, 0, 0, 0, 0, 3.7],
                              [0, 0, 0, 0, 0, 0]])  # Remplacez par votre matrice de précédence réelle





num_tasks = 6
num_population = 1000
num_generations = 1000

list_best_paths = genetic_algorithm(num_tasks, num_population, num_generations, precedence_matrix,execution_time3)

print("Chemin optimal:", list_best_paths)













