from random import random as rnd
from math import sin, pi


class Generation:
    __pairing_possibility = 0
    __mutation_possibility = 0
    __individuals_number = 0
    __gens_number = 8
    __desired_fit = 0.999

    with_debug = True

    def __init__(self, pairing_possibility, mutation_possibility, individuals_number, with_debug=True):
        self.__pairing_possibility = pairing_possibility
        self.__mutation_possibility = mutation_possibility
        self.__individuals_number = individuals_number
        self.with_debug = with_debug

    def run(self):
        population = self.__init_population()
        best_individual = self.__find_the_best({'individual': None, 'fit': 0.0}, population)
        print('formatted', population)
        generation_count = 0
        while best_individual.get('fit') < self.__desired_fit:
            generation_count += 1
            population = self.__selection(population)
            population = self.__pairing(population)
            population = self.__mutation(population)
            best_individual = self.__find_the_best(best_individual, population)
            if self.with_debug:
                print(str(generation_count) + '. fit = ', best_individual.get('fit'))
        print('finish! ', best_individual)
        print('took', generation_count, 'generations')

    def __init_individual(self):
        individual = bin(int(rnd() * 2 ** self.__gens_number - 1))
        return individual

    def __init_population(self):
        return self.__format([self.__init_individual() for x in range(self.__individuals_number)])

    def __fitness_normalized(self, individual, population):
        return self.__fitness(individual) / sum(map(lambda x: self.__fitness(x), population))

    def __fitness(self, individual):
        return sin(pi * int(individual, 2) / 256.0)

    def __selection(self, population):
        chances = [rnd() for x in range(8)]
        next_generation = []
        for chance in chances:
            f_sum1 = 0
            f_sum2 = 0
            for individual in population:
                f_sum2 += self.__fitness_normalized(individual, population)
                if f_sum1 <= chance <= f_sum2:
                    next_generation.append(individual)
                    break
                f_sum1 = f_sum2
        return self.__format(next_generation)

    def __generate_pairs(self, p):
        get_rnd_index = lambda: int(rnd() * (len(p) / 2))
        # individual1 and individual2 to pair, with the pairability
        return [(p.pop(get_rnd_index()), p.pop(get_rnd_index())) for i in range(int(len(p) / 2))]

    def __generate_pivots(self):
        generate_pivot = lambda: int(rnd() * (self.__gens_number - 2) + 1)
        pivot1 = pivot2 = generate_pivot()
        while pivot1 == pivot2:
            pivot2 = generate_pivot()
        # '0bXXXXXXXX' - adjustment for prefix 0b
        pivot1 += 2
        pivot2 += 2
        return (pivot1, pivot2) if pivot1 < pivot2 else (pivot2, pivot1)

    def __pairing(self, population):
        pairs = self.__generate_pairs(population)
        for pair in pairs:
            pairing_chance = rnd()
            if pairing_chance <= self.__pairing_possibility:
                pivot1, pivot2 = self.__generate_pivots()
                gens = [(parent[:pivot1], parent[pivot1:pivot2], parent[pivot2:]) for parent in pair]
                offspring1 = gens[0][0] + gens[1][1] + gens[0][2]
                offspring2 = gens[1][0] + gens[0][1] + gens[1][2]
                population.append(offspring1)
                population.append(offspring2)
            else:
                population.append(pair[0])
                population.append(pair[1])
        return self.__format(population)

    def __mutation(self, population):
        for individual_index in range(self.__individuals_number):
            for gen_index in range(self.__gens_number):
                mutation_chance = rnd()
                if mutation_chance <= self.__mutation_possibility:
                    population = self.__perform_mutation(gen_index, individual_index, population)
        return self.__format(population)

    def __perform_mutation(self, gen_index, individual_index, population):
        mutated = population[individual_index][2:]
        inverted = self.__inverse_bit(mutated[gen_index-2])  # '0b' prefix adjustment
        population[individual_index] = '0b' + mutated[:gen_index] + inverted + mutated[gen_index + 1:]
        return population

    def __inverse_bit(self, bit):
        return '0' if bit == '1' else '1'

    def __find_the_best(self, last_best, p):
        for individual in p:
            individual_fit = self.__fitness(individual)
            if individual_fit > last_best.get('fit'):
                last_best = {'individual': individual, 'fit': individual_fit}
        return last_best

    def __format(self, p):
        return [individual + '0'*(self.__gens_number + 2 - len(individual)) for individual in p]


def main():
    generation1 = Generation(0.75, 0.01, 8)
    generation1.run()
    pass


if __name__ == '__main__':
    main()
