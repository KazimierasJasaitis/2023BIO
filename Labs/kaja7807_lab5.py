import random

# Function to optimize
def objective_function(x):
    # Example objective function
    return -(x - 5)**2 + 10

# Create a population
def create_population(size, bounds):
    return [random.uniform(bounds[0], bounds[1]) for _ in range(size)]

# Crossover (mating)
def crossover(parent1, parent2):
    child = (parent1 + parent2) / 2
    return child

# Mutation
def mutate(individual, bounds, mutation_rate):
    if random.random() < mutation_rate:
        individual += random.uniform(-1, 1)
        individual = max(bounds[0], min(individual, bounds[1]))
    return individual

# Main genetic algorithm
def genetic_algorithm(objective, bounds, population_size, generations, mutation_rate):
    population = create_population(population_size, bounds)
    best_individual = None
    best_fitness = float('-inf')

    for generation in range(generations):
        # Evaluate fitness
        fitness = [objective(ind) for ind in population]

        # Find best individual
        for ind, fit in zip(population, fitness):
            if fit > best_fitness:
                best_fitness = fit
                best_individual = ind

        # Create next generation
        new_population = []
        for _ in range(population_size):
            # Select parents
            parent1, parent2 = random.sample(population, 2)
            # Crossover
            child = crossover(parent1, parent2)
            # Mutation
            child = mutate(child, bounds, mutation_rate)
            new_population.append(child)
        
        population = new_population

    return best_individual, best_fitness

# Parameters
bounds = [0, 10]  # Boundaries for the values
population_size = 1000
generations = 1000
mutation_rate = 0.01

# Run the genetic algorithm
best_individual, best_fitness = genetic_algorithm(objective_function, bounds, population_size, generations, mutation_rate)
print("Best Individual:", best_individual)
print("Best Fitness:", best_fitness)
