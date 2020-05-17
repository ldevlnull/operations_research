from random import random as rnd
from math import sin, pi

PAIRING_POSSIBILITY = 0.75
MUTATION_POSSIBILITY = 0.01
INDIVIDUALS_NUMBER = 8
GENS_NUMBER = 8
DESIRED_FIT = 0.99


def init_individual():
    individual = bin(int(rnd() * 2 ** GENS_NUMBER - 1))
    while len(individual) < GENS_NUMBER + 1:
        individual += '0'
    return individual


def init_population():
    return [init_individual() for x in range(INDIVIDUALS_NUMBER)]


def fitness_normalized(individual, population):
    return fitness(individual) / sum(map(lambda x: fitness(x), population))


# x є [0; 255]
def fitness(x):
    x = int(x, 2)
    return sin(pi * x / 256.0)


def selection(population):
    # chances = [rnd() for x in range(8)]
    chances = [0.293, 0.971, 0.160, 0.469, 0.664, 0.568, 0.371, 0.109]
    next_generation = []
    for chance in chances:
        f_sum1 = 0
        f_sum2 = 0
        for individual in population:
            f_sum2 += fitness_normalized(individual, population)
            if f_sum1 <= chance <= f_sum2:
                next_generation.append(individual)
                break
            f_sum1 = f_sum2
    return next_generation


def generate_pairs(population):
    get_rnd_index = lambda: int(rnd() * (len(population) / 2))
    # individual1 and individual2 to pair, with the pairability
    return [(population.pop(get_rnd_index()), population.pop(get_rnd_index())) for i in
            range(int(len(population) / 2))]


def generate_pivots(gens_number=8):
    generate_pivot = lambda: int(rnd() * (gens_number - 2) + 1)
    pivot1 = pivot2 = generate_pivot()
    while pivot1 == pivot2:
        pivot2 = generate_pivot()
    # '0bXXXXXXXX' - adjustment for prefix 0b
    pivot1 += 2
    pivot2 += 2
    return (pivot1, pivot2) if pivot1 < pivot2 else (pivot2, pivot1)


def pairing(population):
    pairs = generate_pairs(population)
    offsprings = []
    for pair in pairs:
        if rnd() <= PAIRING_POSSIBILITY:
            pivot1, pivot2 = generate_pivots(GENS_NUMBER)
            gens = [(parent[:pivot1], parent[pivot1:pivot2], parent[pivot2:]) for parent in pair]
            offspring1 = gens[0][0] + gens[1][1] + gens[0][2]
            offspring2 = gens[1][0] + gens[0][1] + gens[1][2]
            offsprings.append(offspring1)
            offsprings.append(offspring2)
            pass
        else:
            offsprings.append(pair[0])
            offsprings.append(pair[1])
    return offsprings


def mutation(population):
    for individual_index in range(INDIVIDUALS_NUMBER):
        for gen_index in range(GENS_NUMBER):
            mutation_chance = rnd()
            if mutation_chance <= MUTATION_POSSIBILITY:
                population = perform_mutation(gen_index, individual_index, population)
    return population


def perform_mutation(gen_index, individual_index, population):
    mutated_individual = population[individual_index][2:]
    inverted = inverse_bit(mutated_individual[gen_index])
    population[individual_index] = '0b' + mutated_individual[:gen_index] + inverted + mutated_individual[gen_index + 1:]
    return population


def inverse_bit(bit):
    return '0' if bit == '1' else '1'


def main():
    # p = ['0b10111101', '0b11011000', '0b01100011', '0b11101100', '0b10101110', '0b01001010', '0b00100011', '0b00110101']
    p = init_population()
    print('init: ', p)
    best_individual = find_the_best({'individual': None, 'fit': 0.0}, p)

    generation_count = 0
    while best_individual.get('fit') < DESIRED_FIT:
        generation_count += 1
        p = selection(p)
        p = pairing(p)
        p = mutation(p)
        best_individual = find_the_best(best_individual, p)
        print(str(generation_count) + '. fit = ', best_individual.get('fit'))
    print('finish! ', best_individual)
    print('took', generation_count, 'generations')
    pass


def find_the_best(last_best, p):
    for individual in p:
        individual_fit = fitness(individual)
        if individual_fit > last_best.get('fit'):
            last_best = {'individual': individual, 'fit': individual_fit}
    return last_best


if __name__ == '__main__':
    main()
