# f(x) = -5*x1 - 2*x2 - 18
# x1 - x2 + x3 = 4
# 2*x1 - x3 - x4 = -5
# x1 + x2 - x5 = -4
# x2 + x6 = 5
# 2*x1 - 2*x2 - x6 + 2*x7 = 7
# x1 >= 0, x2 >= 0, x3 >= 0,
# x4 >= 0, x5 >= 0, x6 >= 0, x7 >= 0
"""
Завдання:
- побудувати матрицю системи лінійних рівнянь (A), визначити її ранг;
- побудувати матрицю вільних коефіцієнтів системи (B)
- побудувати розширену матрицю з A і B , знайти її ранг;
- побудувати вертор-градієнт с(x1, x2);
- обчислити оптимальний розв'язок цільової функції.
"""
import numpy as np
import matplotlib.pyplot as plt

# матриця системи лінійних рівнянь
A = np.array([
    [1, -1, 1, 0, 0, 0, 0],
    [2, -1, -1, -1, 0, 0, 0],
    [1, 1, 0, 0, -1, 0, 0],
    [0, 1, 0, 0, 0, 1, 0],
    [2, -2, 0, 0, 0, -1, 2]
])
print('rang A: ', np.linalg.matrix_rank(A))

# матриця вілних коефіцієнтів
b = np.array([4, -5, -4, 5, 7])
B = b.reshape(-1, 1)

# розширена матриця
AB = np.append(A, B, axis=1)
print('rang AB: ', np.linalg.matrix_rank(AB))

x1 = np.arange(-1, 15, 0.5)
x2 = [x1 - 4, 1.5 * x1 + 0.5, 2 * x1 - 12, [5] * len(x1), -2.5 * x1, 0.4 * x1]
x2_str = ['x1-4', '1.5*x1+0.5', '2*x1-12', '5', '-2.5*x1']
fig, ax = plt.subplots()
plt.grid(True)
for i in range(len(x2) - 1):
    ax.plot(np.around(x1, decimals=2), np.around(x2[i], decimals=2), label='x2= ' + str(x2_str[i]))
plt.xlabel('x1')
plt.ylabel('x2')
ax.xaxis
ax.set_aspect(aspect='equal', anchor="C")
ax.set_xlim([-5, 10])
ax.set_ylim([-2, 10])
plt.axhline(0)
plt.axvline(0)

for i in range(20, 30, 2):
    ax.plot(x1, -2.5 * x1 + i, 'b:', linewidth=2)
plt.legend(fontsize=8)
# будуємо вектор-градієнт
plt.quiver(0, 0, 2, 1, scale=8)
plt.show()