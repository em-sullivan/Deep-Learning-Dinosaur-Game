'''
Genetic algorithm functions
for creating an AI to play
the Dinosaur game

NOTE: This still needs to be tested, and propbably doesn't work
for now
'''

import numpy as np
import random

def model_crossover(current_pool, parent_1, parent_2):
    '''
    Produce offspring based on the best parents
    '''
    # Weight of parents
    weight1 = current_pool[parent_1].get_weights()
    weight2 = current_pool[parent_2].get_weights()
    new_weight1 = weight1
    new_weight2 = weight2

    # Gene
    gene = random.randint(0, len(new_weight1) - 1)

    new_weight1[gene] = weight2[gene]
    new_weight2[gene] = weight1[gene]
    return np.asarray([new_weight1, new_weight2])

def model_mutate(weights):
    '''
    Mutate the weights of a model
    '''
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            if (random.uniform(0, 1) > .7):
                change = random.uniform(-.5,.5)
                weights[i][j] += change
    
    return weights

def roulette_selection(fitness, total_fitness, pop_size):
    choice = random.randint(0, total_fitness)
    parent = 0

    current = 0
    for idx in range(pop_size):
        current += fitness[idx]
        if current > choice:
            parent = idx
            break

    return parent


def genetic_updates(current_pool, fitness, pop_size):

    new_weights = []
    # Calculate total fitness
    total_fitness = sum(fitness)
    
    # Breeding time
    for i in range(pop_size // 2):
        # Pick two parents
        parent_1 = roulette_selection(fitness, total_fitness, pop_size)
        parent_2 = roulette_selection(fitness, total_fitness, pop_size)
  
        # Model crossover between two parents
        new = model_crossover(current_pool, parent_1, parent_2)
        
        # Mutate models
        update_w1 = model_mutate(new[0])
        update_w2 = model_mutate(new[1])
        new_weights.append(update_w1)
        new_weights.append(update_w2)

    # Set new weights, reset fitness
    for i in range(len(new_weights)):
        current_pool[i].set_weights(new_weights[i])
    return