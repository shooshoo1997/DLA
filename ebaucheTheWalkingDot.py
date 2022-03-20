import numpy as np
import matplotlib.pyplot as plt
import random as rd

def randomWalker(n:int, N:int, L:int):
    x = np.zeros((N+1, n))
    y = np.zeros((N+1, n))

    for j in range(0, n):
        for i in range(1, N+1):
            a = True
            while(a):
                dir = rd.randint(1, 4)
                if dir == 1 and y[i, j] < (L-1)/2:
                    y[i:, j] += 1
                    a = False
                elif dir == 2 and y[i, j] < (L-1)/2:
                    x[i:, j] += 1
                    a = False
                elif dir == 3 and y[i, j] > -(L-1)/2:
                    y[i:, j] += -1
                    a = False
                elif dir == 4 and y[i, j] > -(L-1)/2:
                    x[i:, j] += -1
                    a = False
    return x, y


if __name__ == '__main__':
    randomWalk = randomWalker(10000, 500, 101)
    posX = randomWalk[0]
    posY = randomWalk[1]
    module = np.sqrt((posY[-1, :]**2) + (posX[-1, :]**2))

    plt.figure(1)
    plt.hist(module, bins='auto', density=True, facecolor='g')
    plt.show()
