# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 21:51:30 2018

@author: rfrench
"""

import random
from enum import Enum, unique

MIN_FITNESS = -100000000

def binary_mutation(solution, mutation_prob):
    new_solution = []
    for i in solution:
        new_solution.append(i ^ (random.random() < mutation_prob))
    return new_solution
    
def generate_children(population, parameters):
    parents = selection(population, parameters)
    children = []
    for i in range(len(parents) // 2):
        p1, p2 = parents[i * 2], parents[i * 2 + 1]
        for c in crossover(p1, p2, parameters.crossover):
            children.append(parameters.mutation_func(c, parameters.mutation_rate))
    
    return children

def crossover(p1, p2, crossover_method):
    if crossover_method == Crossover.ARITHMETIC:
        return arithmetic_crossover(p1, p2)
    else:
        return one_point_crossover(p1, p2)
    
def arithmetic_crossover(p1, p2):
    if type(p1[0]) is list:
        crossover_idx = random.randint(0, len(p1) - 1)
        c1 = list(p1[0][:crossover_idx])
        c2 = list(p2[0][:crossover_idx])
        for i in range(crossover_idx, len(p1)):
            weight = random.random()
            total = p1[0][i] + p2[0][i]
            c1.append(weight * total)
            c2.append((1 - weight) * total)
        return c1, c2
    else:
        weight = random.random()
        total = p1[0] + p2[0]
        c1 = weight * total
        c2 = (1 - weight) * total
        return c1, c2

def one_point_crossover(p1, p2):
    crossover_idx = random.randint(0, len(p1) - 1)
    c1 = p1[0][:crossover_idx] + p2[0][crossover_idx:]
    c2 = p2[0][:crossover_idx] + p1[0][crossover_idx:]
    return c1, c2

def survival(current_population, pop_size, survival_method):
    if survival_method == Survival.TOURNAMENTWITHELITEISM:
        return tournament_with_eliteism(current_population, pop_size)
    else:
        return tournament_survival(current_population, pop_size)

def tournament_survival(current_population, pop_size):
    new_pop = []
    for i in range(pop_size):
        strats = random.sample(current_population, 2)
        new_pop.append(better_strategy(*strats))
    return new_pop

def tournament_with_eliteism(current_population, pop_size):
    new_pop = sorted(current_population, key=lambda s: s[1])[len(current_population) - 10 : len(current_population)]
    return new_pop + tournament_survival(current_population, pop_size - 10)

def selection(current_population, parameters):
    if parameters.selection == Selection.ROULETTE:
        return roulette_selection(current_population, parameters.num_children * 2)
    elif parameters.selection == Selection.RANKEDROULETTE:
        return ranked_roulette_selection(current_population, parameters.num_children * 2)
    elif parameters.selection == Selection.WEIGHTEDROULETTE:
        return weighted_ranked_roulette_selection(current_population, parameters.num_children * 2)
    else:
        return random.choices(current_population, k=parameters.num_children * 2)

def roulette_selection(current_population, num_strats):
    return random.choices(current_population, weights=[s[1] for s in current_population], k=num_strats)

def weighted_ranked_roulette_selection(current_population, num_strats, alpha):
    pop_size = len(current_population)
    R = pop_size * (pop_size - 1) / 2
    w = [alpha / pop_size + (1 - alpha) * r / R for r in range(len(current_population))]
    random.choices(sorted(current_population, key=lambda s: s[1]), weights=w, k=num_strats)

def ranked_roulette_selection(current_population, num_strats):
    return random.choices(sorted(current_population, key=lambda s: s[1]), weights=range(len(current_population)), k=num_strats)

def better_strategy(strat1, strat2):
    if strat1[1] > strat2[1]:
        return strat1
    return strat2

def best_strategy(population):
    max_fitness = MIN_FITNESS
    best_strategies = []
    for strat in population:
        if (strat[1] == max_fitness):
            best_strategies.append(strat)
        elif (strat[1] > max_fitness):
            max_fitness = strat[1]
            best_strategies = [strat]
    return random.choice(best_strategies)

def choose_candidates(current_populations):
    return [best_strategy(population)[0] for population in current_populations]

def multipop_fitness_update(candidates, populations, fitness_func):
    for population_idx in range(len(populations)):
        for strat in populations[population_idx]:
            local_candidates = list(candidates)
            local_candidates[population_idx] = strat[0]
            strat[1] = fitness_func(local_candidates)[population_idx]
    return populations

def ga_iteration(current_populations, parameters):
    candidate_strategies = choose_candidates(current_populations)
    current_populations = multipop_fitness_update(candidate_strategies, current_populations, parameters.fitness_func)
    children = [[[child, MIN_FITNESS] for child in generate_children(population, parameters)] for population in current_populations]
    children = multipop_fitness_update(candidate_strategies, children, parameters.fitness_func)
    total_populations = [parents + children for (parents, children) in zip(current_populations, children)]
    return [survival(population, parameters.population_size, parameters.survival) for population in total_populations]

def ga_optimize(init_populations, parameters):
    current_populations = [[[s, MIN_FITNESS] for s in pop] for pop in init_populations]
    for i in range(parameters.iterations):
        current_populations = ga_iteration(current_populations, parameters)
    return [sorted(population, key=lambda s: s[1])[-1] for population in current_populations]

@unique
class Crossover(Enum):
    ONEPOINT = 1
    ARITHMETIC = 2
   
@unique
class Survival(Enum):
    TOURNAMENT = 1
    TOURNAMENTWITHELITEISM = 2
    
@unique
class Selection(Enum):
    ROULETTE = 1
    RANKEDROULETTE = 2
    WEIGHTEDROULETTE = 3
    
class Parameters:
    iterations = 1000
    population_size = 100
    num_children = 100
    mutation_rate = 0.1
    crossover = Crossover.ONEPOINT
    survival = Survival.TOURNAMENT
    selection = Selection.ROULETTE
    mutation_func = binary_mutation
    fitness_func = lambda x: 0