import math as m
import pylab as pl
import sympy as sp
import numpy as np


def z_function(x, y, n):
    return (x * y + 50 / x + 20 / y) if 1 else (x ** 2 + y ** 2 - 2 * m.log(x) - 18 * m.log(y))


def u_function(x, y, z):
    return x + y / x + z / y + 2 / z


def get_extremum(n):
    x, y, z = sp.symbols('x y z', real=True)
    if n == 1:
        f = x * y + 50 / x + 20 / y
    elif n == 2:
        f = x ** 2 + y ** 2 - 2 * sp.log(x) - 18 * sp.log(y)
    elif n == 3:
        f = x + y / x + z / y + 2 / z
    dx = sp.diff(f, x)
    dy = sp.diff(f, y)
    print("f'x =", dx)
    print("f'y =", dy)
    if n == 3:
        dz = sp.diff(f, z)
        print("f'z =", dz)
        E = sp.solve((dx, dy, dz), (x, y, z))
    else:
        E = sp.solve((dx, dy), (x, y))
    print("Extremum:", E)
    dxx = sp.diff(dx, x)
    dyx = sp.diff(dy, x)
    dxy = sp.diff(dx, y)
    dyy = sp.diff(dy, y)
    print("f''xx =", dxx)
    print("f''xy =", dxy)
    print("f''yx =", dyx)
    print("f''yy =", dyy)
    if n == 3:
        dxz = sp.diff(dx, z)
        dyz = sp.diff(dx, z)
        dzx = sp.diff(dz, x)
        dzy = sp.diff(dz, y)
        dzz = sp.diff(dz, z)
        print("f''xz =", dxz)
        print("f''yz =", dyz)
        print("f''zx =", dzx)
        print("f''zy =", dzy)
        print("f''zz =", dzz)
    for i in range(len(E)):
        print("Extremum: ", E[i])
        if n == 3:
            matrix = np.array([
                [
                    sp.N(dxx.subs([(x, sp.N(E[i][0])), (y, sp.N(E[i][1])), (z, sp.N(E[i][2]))])),
                    sp.N(dxy.subs([(x, sp.N(E[i][0])), (y, sp.N(E[i][1])), (z, sp.N(E[i][2]))])),
                    sp.N(dxz.subs([(x, sp.N(E[i][0])), (y, sp.N(E[i][1])), (z, sp.N(E[i][2]))]))
                ], [
                    sp.N(dyx.subs([(x, sp.N(E[i][0])), (y, sp.N(E[i][1])), (z, sp.N(E[i][2]))])),
                    sp.N(dyy.subs([(x, sp.N(E[i][0])), (y, sp.N(E[i][1])), (z, sp.N(E[i][2]))])),
                    sp.N(dyz.subs([(x, sp.N(E[i][0])), (y, sp.N(E[i][1])), (z, sp.N(E[i][2]))]))
                ], [
                    sp.N(dzx.subs([(x, sp.N(E[i][0])), (y, sp.N(E[i][1])), (z, sp.N(E[i][2]))])),
                    sp.N(dzy.subs([(x, sp.N(E[i][0])), (y, sp.N(E[i][1])), (z, sp.N(E[i][2]))])),
                    sp.N(dzz.subs([(x, sp.N(E[i][0])), (y, sp.N(E[i][1])), (z, sp.N(E[i][2]))]))
                ]
            ])
        else:
            matrix = np.array([
                [
                    sp.N(dxx.subs([(x, sp.N(E[i][0])), (y, sp.N(E[i][1]))])),
                    sp.N(dxy.subs([(x, sp.N(E[i][0])), (y, sp.N(E[i][1]))]))
                ], [
                    sp.N(dyx.subs([(x, sp.N(E[i][0])), (y, sp.N(E[i][1]))])),
                    sp.N(dyy.subs([(x, sp.N(E[i][0])), (y, sp.N(E[i][1]))]))
                ]
            ])
        matrix = matrix.astype(np.float64)
        d = np.linalg.det(matrix)
        if d < 0:
            print("No extrema. d =", d)
        elif d > 0:
            print("Extrema exists. d =", d)
            if n == 1:
                A = z_function(sp.N(E[i][0]), sp.N(E[i][1]), 1)
                print("z(matrix) =", A)
            elif n == 2:
                if (sp.N(E[i][0]) <= 0) or (sp.N(E[i][1]) <= 0):
                    break
                else:
                    A = z_function(sp.N(E[i][0]), sp.N(E[i][1]), 2)
                    print("z(matrix) =", A)
            elif n == 3:
                A = u_function(sp.N(E[i][0]), sp.N(E[i][1]), sp.N(E[i][2]))
                print("u(matrix) =", A)
            else:
                print("Insufficient information", d)

            if len(E) <= 0:
                print("No extremum exists")


def main():
    zf = np.vectorize(z_function)
    get_extremum(1)
    x, y = np.arange(0.1, 7.0, 0.1), np.arange(0.1, 7.0, 0.1)
    X, Y = pl.meshgrid(x, y)
    Z = zf(X, Y, 1)
    im = pl.imshow(Z, cmap=pl.cm.RdBu)
    cset = pl.contour(Z, np.arange(21, 100, 10), linewidths=2, cmap=pl.cm.Set2)

    pl.clabel(cset, inline=True, fmt='%1.1f', fontsize=15)
    pl.colorbar(im)
    pl.title('z = x*y + 50/x + 20/y')
    pl.show()

    print()

    get_extremum(2)
    x = np.arange(0.1, 5.0, 0.1)
    y = np.arange(0.1, 5.0, 0.1)
    X, Y = pl.meshgrid(x, y)
    Z = zf(X, Y, 2)
    im = pl.imshow(Z, cmap=pl.cm.RdBu)
    cset = pl.contour(Z, np.arange(-10, 0, 1), linewidths=3, cmap=pl.cm.Set2)
    pl.clabel(cset, inline=True, fmt='%1.1f', fontsize=10)
    pl.colorbar(im)
    pl.title('z = x^2 + y^2 - 2*log(x) - 18*log(y)')
    pl.show()
    print()
    get_extremum(3)


if __name__ == '__main__':
    main()
