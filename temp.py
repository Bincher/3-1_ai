import numpy as np

a1 = np.array([5,3,6,7,1])

a2 = np.arange(1,11)
a3 = np.arange(10, -9, -2)
a4 = np.random.randint(5,size = 1) + 1

a5 = (5 - 1) * np.random.rand(3, 3) + 1

print(a1,a2,a3,a4,a5)

m = np.array([[0, 1, 2, 3, 4],
                         [5, 6, 7, 8, 9],
                         [10, 11, 12, 13, 14]])
m[1][2] = 70
m[2][:2] = [100,110]
m[:2,3:] = [[300, 400], [800, 900]]
mask = (m % 2 == 0) & (m % 3 == 0)
b1 = m[mask]
print(m)
print(b1)