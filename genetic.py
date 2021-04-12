'''
Genetic algorithm functions
for creating an AI to play
the Dinosaur game

NOTE: This still needs to be tested, and propbably doesn't work
for now
'''

import numpy as np
import random

def model_crossover(parent_1, parent_2):
    '''
    Produce offspring based on parents
    '''

    new_genes1 = parent_1 
    new_genes2 = parent_2

    gene = random.randint(0, len(new_genes1) - 1)

    new_genes1[gene] = parent_2[gene]
    new_genes2[gene] = parent_1[gene]
    return np.asarray([new_genes1, new_genes2])

def mutate(chromosome):
    '''
    Mutate the genes chromosome by randomly modifying values.
    For the dino game, its the weights of the NN
    '''
    for in range(len(chromosome)):
        for j in range(leng(chromosome[i])):
            if (random.uniform(0, 1) > 0.7):
                change = random.uniform(-0.5, 0.5)
                chromosome[i][j] += change

def roulette_selection(fitness, total_fitness):
    '''
    Choose a random Chromosome from the population.
    Has a higher chance of picking one with a higher fitness value
    '''

    choice = random.randint(0, total_fitness)
    chromosome = 0
    current = 0

    # This currentlly assumes that the fitness is a list
    # of fitness values
    for idx in range(len(fitness)):
        current += fitness[idx]
        if current > choice:
            chromosome = idx
            break
    
    # Index of chromosome in population
    return idx


def genetic_algorithm(population, fitness):
    '''
    Peform genetic algorithm, do model corssover,
    mutation, generate new population
    '''

    # Calculate total fintess for roulette selection
    total_fitenss = sum(fitness)
    new_population = []
    
    # Generate new population
    for i in range(len(population) // 2):

        # Pick two parents from random selection
        parent_1 = roulette_selection(fitness, total_fitness)
        parent_2 = roulette_selection(fitness, total_fitness)

        # Model crossover
        new = model_corssover(population[parent_1], population[parent_2])

        # Mutation
        update_g1 = mutate(new[0])
        update_g2 = mutate(new[1])
        new_population.append(update_g1)
        new_population.append(update_g2)

    
    # Set new popluation
    for i in range(len(population)):
        population[i] = new_population[i]