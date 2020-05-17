# F(x1, x2) = 2x1 + 3x2   -----  max
# x1 + x2 <= 100
# 2x1 +x2 <= 180
# x1 + 2*x2 <= 160
# де x1, x2, x3, x4, x5 >= 0, F(x1, x2) = 2x1 + 3x2   -----  max

import numpy as np
import matplotlib.pyplot as plt

A = np.array([[1,1,1,0,0],
              [2,1,0,1,0],
              [1,2,0,0,1],
              ])
print('rang A: ',np.linalg.matrix_rank(A))

b = np.array([100, 180, 160])
B = b.reshape(-1,1)
AB = np.append(A, B, axis=1)
print('rang AB: ',np.linalg.matrix_rank(AB))

x1 = np.arange(-1,200,10)
x2 = [100-x1, 180-(2*x1), 80-(x1/2)]
x2_str = ['100-x1', '180-2*x1', '80 - x1/2']
fig, ax = plt.subplots()
plt.grid(True)
for i in range(len(x2)):
    ax.plot(np.around(x1, decimals=2), np.around(x2[i], decimals=2), label='x2= '+ str(x2_str[i]))
plt.xlabel('x1')
plt.ylabel('x2')
ax.xaxis
ax.set_aspect(aspect='equal', anchor="C")
ax.set_xlim([-5, 200])
ax.set_ylim([-2, 200])
plt.axhline(0)
plt.axvline(0)

for  i in range(0, 100, 10):
    ax.plot(x1, (-2*x1/3)+i,'b:', linewidth=2)    
plt.legend(fontsize=8)
plt.quiver(2, 3, scale=10, color='green') 
plt.show()