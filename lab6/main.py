from numpy import min, array


def pid(x):
    p = min(x)
    if p >= 0:
        return -1
    i = 2
    while x[i] != p:
        i += 1
    return i


def find_min(x, i):
    p = 0
    for j in range(4):
        if p == 0 and x[j + 1][i] > 0:
            m = abs(x[j + 1][1] / x[j + 1][i])
            p = j + 1
        elif x[j + 1][i] > 0 and m > abs(x[j + 1][1] / x[j + 1][i]):
            m = abs(x[j + 1][1] / x[j + 1][i])
            p = j + 1
    return p


def main():
    q = k = p = b = o = 0
    x = array([
        [0, 0, 1, 2, 3],
        [7, 0, -35, -45, - 55],
        [4, 550, 20, 15, 20],
        [5, 900, 27, 35, 50],
        [6, 550, 10, 5, 10.]
    ])

    j = 0
    while j == 0:
        i = pid(x[1])
        if i == -1:
            j = 1
        else:
            p = find_min(x, i)
            if p == 0:
                break
            o = x[p][i]
            b = array([
                x[0],
                [x[1][0], 0, 0, 0, 0],
                [x[2][0], 0, 0, 0, 0],
                [x[3][0], 0, 0, 0, 0],
                [x[4][0], 0, 0, 0, 0]
            ])
            b[0][i] = x[p][0]
            b[p][0] = x[0][i]
            q = k = 1
        while k != 5 or q != 5:
            if k == 5:
                k = 1
                q += 1
                if q == 5:
                    k = 5
            if q == 5:
                break
            if k == i and q == p:
                b[q][k] = 1 / x[q][k]
            elif k == i:
                b[q][k] = -x[q][k] / o
            elif q == p:
                b[q][k] = x[q][k] / o
            else:
                b[q][k] = (x[q][k] * o - x[q][i] * x[p][k]) / o
            k += 1
        x = b

    print('Win =', x[1][1])
    print('f =', x[1][1])
    print('x1 =', x[2][1])
    print('x2 =', x[3][1])
    print('x3 =', x[4][1])


if __name__ == '__main__':
    main()
