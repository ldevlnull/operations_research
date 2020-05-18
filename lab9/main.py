from math import sin, pi
from random import random as rnd
import matplotlib.pyplot as plt


class Generation:
    __max_epochs = 1_000
    __pairing_possibility = 0
    __mutation_possibility = 0
    __individuals_number = 0
    __gens_number = 8
    __desired_fit = 0
    __f = None

    with_debug = True

    def __init__(self, pairing_possibility, mutation_possibility, individuals_number, fitness, desired_fit, with_debug=False):
        self.__pairing_possibility = pairing_possibility
        self.__mutation_possibility = mutation_possibility
        self.__individuals_number = individuals_number
        self.__f = fitness
        self.__desired_fit = desired_fit
        self.with_debug = with_debug

    def run(self):
        population = self.__init_population()
        best_individual = self.__determine_best_individual({
            'individual': population[0],
            'fit': self.__fitness(population[0])
        }, population)
        generation_count = 0
        while best_individual.get('fit') < self.__desired_fit:
            generation_count += 1
            self.__log(('init' if generation_count == 1 else ''), 'population\t', population)
            population = self.__selection(population)
            self.__log('after selection\t', population)
            population = self.__pairing(population)
            self.__log('after partition\t', population)
            population = self.__mutation(population)
            self.__log('after mutation\t', population)
            best_individual = self.__determine_best_individual(best_individual, population)
            self.__update_plot(population)
            if self.with_debug:
                self.__log(str(generation_count) + '. fit = ', best_individual.get('fit'))
            self.__log('============================', '\n')
            if generation_count > self.__max_epochs:
                print('Couldn\'t reach required fit', self.__desired_fit, 'for', generation_count, 'epochs!')
                break
        print('finish! ', best_individual)
        print('took', generation_count, 'generations')

    def __init_population(self):
        return self.__format([self.__init_individual() for x in range(self.__individuals_number)])

    def __init_individual(self):
        individual = bin(int(rnd() * 2 ** self.__gens_number))
        return individual

    def __determine_best_individual(self, last_best, p):
        for individual in p:
            individual_fit = self.__fitness(individual)
            if individual_fit > last_best.get('fit'):
                last_best = {'individual': individual, 'fit': individual_fit}
        return last_best

    def __fitness_normalized(self, individual, population):
        sum = 0
        for i in population:
            sum += self.__fitness(i)
        return self.__fitness(individual) / sum

    def __fitness(self, individual):
        return self.__f(int(individual, 2))

    def __selection(self, population):
        chances = [rnd() for x in range(self.__individuals_number)]
        next_generation = []
        for chance in chances:
            f_sum1 = 0
            f_sum2 = 0
            for individual in population:
                f_sum2 += self.__fitness_normalized(individual, population)
                if f_sum1 <= chance <= f_sum2 or f_sum2 <= chance <= f_sum1:
                    next_generation.append(individual)
                    break
                f_sum1 = f_sum2
        return self.__format(next_generation)

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

    def __generate_pairs(self, p):
        get_rnd_index = lambda: int(rnd() * (len(p) / 2))
        # individual1 and individual2 to pair, with the pairability
        return [(p.pop(get_rnd_index()), p.pop(get_rnd_index())) for i in range(int(len(p) / 2))]

    def __generate_pivots(self):
        generate_pivot = lambda: int(rnd() * (self.__gens_number - 2) + 3)
        pivot1 = pivot2 = generate_pivot()
        while pivot1 == pivot2:
            pivot2 = generate_pivot()
        return (pivot1, pivot2) if pivot1 < pivot2 else (pivot2, pivot1)

    def __mutation(self, population):
        for individual_index in range(self.__individuals_number):
            for gen_index in range(self.__gens_number):
                mutation_chance = rnd()
                if mutation_chance <= self.__mutation_possibility:
                    population = self.__perform_mutation(gen_index, individual_index, population)
        return self.__format(population)

    def __perform_mutation(self, gen_index, individual_index, population):
        mutated = population[individual_index][2:]
        inverted = self.__inverse_bit(mutated[gen_index - 2])  # '0b' prefix adjustment
        population[individual_index] = '0b' + mutated[:gen_index] + inverted + mutated[gen_index + 1:]
        return population

    def __inverse_bit(self, bit):
        return '0' if bit == '1' else '1'

    def __format(self, p):
        return ['0b' + '0' * (self.__gens_number + 2 - len(individual)) + individual[2:] for individual in p]

    def __log(self, *args):
        if self.with_debug:
            text = ''
            for arg in args:
                if arg != '':
                    text += str(arg) + ' '
            print(text.rstrip())



    def __update_plot(self, population):
        yf = [0.0] * 256
        for x in range(256):
            yf[x] = self.__fitness(bin(x))

        plt.plot(yf)
        plt.plot([0, self.__desired_fit], [0, 0])
        plt.xlabel('x')
        plt.ylabel('fit')

        x, y = [], []
        for i in population:
            x = int(i, 2)
            y = self.__fitness(i)
        plt.scatter(x, y, marker='.', c='green', s=30)
        plt.draw()
        plt.show()


def main():
    # general example
    # n = 8
    # pc = 0.75
    # pm = 0.001
    # f = lambda x: sin(pi * x / 256.0)
    # desired = 0.99
    # variant
    n = 24
    pc = 0.62
    pm = 0.005
    desired = -0.9
    f = lambda x: -((3 * (x ** 2) - 15) ** 2) / 256

    generation1 = Generation(pc, pm, n, f, desired, True)
    generation1.run()
    pass


if __name__ == '__main__':
    main()
