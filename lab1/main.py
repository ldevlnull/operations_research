from numpy import mean
from sys import argv

try:
    SELECTED_DATASET = int(argv[1])
except IndexError:
    SELECTED_DATASET = 0

data = [
    {
        0: 4.7060,
        0.1: 4.332,
        0.2: 4.8769,
        0.5: 5.5462,
        0.9: 6.797,
        1.5: 9.3235,
        2.9: 13.3948,
        3: 13.3171,
        3.3: 14.8502
    },
    {
        -1.32: 9.3513,
        -0.5: 4.7551,
        -0.35: 4.256,
        -0.3: 4.1991,
        -0.13: 3.5409,
        0.56: 0.1593,
        0.8: -1.4528,
        1: -2.8614,
        1.15: -3.6007
    }
]

data_answers = [
    {
        'a': 4,
        'b': 3
    },
    {
        'a': 2,
        'b': -5
    }
]


def approximate():
    input_data = data[SELECTED_DATASET]
    xs, ys = list(input_data.keys()), list(input_data.values())
    x_avg, y_avg = mean(xs), mean(ys)

    xy_avg = mean([x * y for x, y in input_data.items()])
    x_square_avg = mean([x * x for x in xs])

    b = (xy_avg - x_avg * y_avg) / (x_square_avg - x_avg * x_avg)
    a = y_avg - b * x_avg

    return a, b


def calculate_error(real_a, real_b):
    a_error = abs(data_answers[SELECTED_DATASET]['a'] - real_a)
    b_error = abs(data_answers[SELECTED_DATASET]['b'] - real_b)
    return a_error, b_error


def main():
    a, b = approximate()
    print('a =', a)
    print('b =', b)
    a_eps, b_eps = calculate_error(a, b)
    print('error: a =', a_eps, '\tb =', b_eps)


if __name__ == '__main__':
    main()
