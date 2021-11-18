import multipopulation_genetic_algorithm as ga
import random

def random_duopoly_solution():
    return random.randint(0, 40)

def market_price(total_quantity):
    return 40 - total_quantity

def profit(price, quantity):
    return price * quantity - 10 * quantity

def fitness(quantities):
    price = market_price(sum(quantities))
    return [profit(price, q) for q in quantities]

def duopoly_mutation(solution, mutation_prob):
    if (random.random() < mutation_prob):
        return max(0, min(40, solution + random.randint(-2,2)))
    else:
        return solution

parameters = ga.Parameters
parameters.crossover = ga.Crossover.ARITHMETIC
parameters.selection = ga.Selection.RANKEDROULETTE
parameters.mutation_func = duopoly_mutation
parameters.fitness_func = fitness
parameters.mutation_rate = 0.03
parameters.population_size = 10
parameters.num_children = 10
parameters.iterations = 100000

populations = [[random_duopoly_solution() for _ in range(parameters.population_size)]  for _ in range(2)]

# populations = [[[s, -1000000] for s in pop] for pop in populations]
# candidates = ga.choose_candidates(populations)
# current_populations = ga.multipop_fitness_update(candidates, populations, parameters.fitness_func)
# children = [[[child, -1000000] for child in ga.generate_children(population, parameters)] for population in current_populations]
# children = ga.multipop_fitness_update(candidates, children, parameters.fitness_func)
# total_populations = [parents + children for (parents, children) in zip(current_populations, children)]
# new_pop = [ga.survival(population, parameters.population_size, parameters.survival) for population in total_populations]
# print(new_pop)


print(populations)
optimal_strat = ga.ga_optimize(populations, parameters)
print(optimal_strat)