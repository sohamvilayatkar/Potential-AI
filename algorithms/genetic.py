"""
Genetic Algorithm (GA) Implementation.
Unit 4: Informed and Local Search.
Demonstrates population evolution, fitness evaluation, selection, crossover, and mutation.
"""

import random
from typing import Dict, List, Any

def decode_chromosome(binary_str: str, min_val: float = 0.0, max_val: float = 31.0) -> float:
    """Decode a 5-bit binary string to an integer/float value."""
    int_val = int(binary_str, 2)
    return float(int_val)

def fitness_function(x: float) -> float:
    """Objective fitness function: f(x) = x^2 - 2*x + 10"""
    return round(x**2 - 2*x + 10, 2)

def genetic_algorithm_optimize(
    population_size: int = 10,
    chromosome_length: int = 5,
    generations: int = 15,
    crossover_rate: float = 0.8,
    mutation_rate: float = 0.05
) -> Dict[str, Any]:
    """
    Executes a simple educational Genetic Algorithm to maximize f(x) = x^2 - 2*x + 10 over [0, 31].
    """
    # 1. Initialize random binary population
    random.seed(42)
    population = [
        "".join(random.choice(["0", "1"]) for _ in range(chromosome_length))
        for _ in range(population_size)
    ]

    generation_history = []
    global_best_individual = None
    global_best_fitness = -float('inf')

    for gen in range(1, generations + 1):
        # 2. Evaluate Fitness
        decoded_vals = [decode_chromosome(ind) for ind in population]
        fitnesses = [fitness_function(x) for x in decoded_vals]

        # Track generation best
        gen_max_fit = max(fitnesses)
        best_idx = fitnesses.index(gen_max_fit)
        gen_best_ind = population[best_idx]
        gen_best_x = decoded_vals[best_idx]
        avg_fitness = round(sum(fitnesses) / len(fitnesses), 2)

        if gen_max_fit > global_best_fitness:
            global_best_fitness = gen_max_fit
            global_best_individual = gen_best_ind

        generation_history.append({
            "generation": gen,
            "best_chromosome": gen_best_ind,
            "best_x": gen_best_x,
            "max_fitness": gen_max_fit,
            "avg_fitness": avg_fitness,
            "sample_population": [
                {"binary": population[i], "x": decoded_vals[i], "fitness": fitnesses[i]}
                for i in range(min(5, len(population)))
            ]
        })

        # 3. Selection (Roulette Wheel / Fitness Proportional)
        total_fitness = sum(fitnesses) if sum(fitnesses) > 0 else 1
        probs = [f / total_fitness for f in fitnesses]
        
        # Cumulative probabilities
        cum_probs = []
        c = 0
        for p in probs:
            c += p
            cum_probs.append(c)

        selected_pop = []
        for _ in range(population_size):
            r = random.random()
            for idx, cp in enumerate(cum_probs):
                if r <= cp:
                    selected_pop.append(population[idx])
                    break
            else:
                selected_pop.append(population[-1])

        # 4. Crossover (Single-Point Crossover)
        next_population = []
        for i in range(0, population_size, 2):
            parent1 = selected_pop[i]
            parent2 = selected_pop[(i + 1) % population_size]

            if random.random() < crossover_rate and chromosome_length > 1:
                point = random.randint(1, chromosome_length - 1)
                child1 = parent1[:point] + parent2[point:]
                child2 = parent2[:point] + parent1[point:]
            else:
                child1, child2 = parent1, parent2

            next_population.extend([child1, child2])

        # 5. Mutation (Bit Flip)
        mutated_population = []
        for ind in next_population[:population_size]:
            mutated_bits = []
            for bit in ind:
                if random.random() < mutation_rate:
                    mutated_bits.append("1" if bit == "0" else "0")
                else:
                    mutated_bits.append(bit)
            mutated_population.append("".join(mutated_bits))

        population = mutated_population

    best_decoded_x = decode_chromosome(global_best_individual)
    return {
        "algorithm": "Genetic Algorithm (GA)",
        "type": "Evolutionary / Stochastic Optimization",
        "objective_function": "f(x) = x^2 - 2*x + 10 (Domain: [0, 31])",
        "population_size": population_size,
        "chromosome_length": f"{chromosome_length} bits",
        "generations": generations,
        "crossover_rate": crossover_rate,
        "mutation_rate": mutation_rate,
        "best_chromosome": global_best_individual,
        "best_solution_x": best_decoded_x,
        "optimal_fitness": global_best_fitness,
        "generation_history": generation_history,
        "biological_analogy": {
            "Chromosome": "Binary Bit String (Genotype)",
            "Fitness": "Objective Score Evaluation",
            "Selection": "Survival of the Fittest (Roulette Wheel)",
            "Crossover": "Recombination of Genetic Traits",
            "Mutation": "Random Bit Flipping for Diversity"
        }
    }
