import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random as rd
import time
import numpy.ma as ma
from beartype import beartype
import matplotlib.ticker as ticker
# from randomwalk import WalkingDot


class DLA:

    def __init__(self):

        self.possible_displacement = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
        self.L = None
        self.posX = 0  # Array for the X position of each dot at each step
        self.posY = 0  # Array for the Y position of each dot at each step
        self.endPosition = None

    def displacement(self, possible_displacement):

        rng = np.random.default_rng()

        return rng.choice(possible_displacement).T

    def checkLimitBreak(self, posX, posY):

        boolX = np.where((-1*(self.L - 1) / 2 <= posX) & (posX <= (self.L - 1) / 2), True, False)
        boolY = np.where((-1*(self.L - 1) / 2 <= posY) & (posY <= (self.L - 1) / 2), True, False)

        return boolX, boolY

    def doParcour(self):

        self.posX = 0
        self.posY = 0
        canMove = True

        while(canMove):

            vector_displacement = self.displacement(self.possible_displacement)
            self.posX += vector_displacement[0]
            self.posY += vector_displacement[1]
            limitSate = self.checkLimitBreak(self.posX, self.posY)
            if (limitSate[0] == False or limitSate[1] == False) == True :
                canMove = False
                if self.endPosition is None:
                    self.endPosition = np.array([self.posX - vector_displacement[0], self.posY - vector_displacement[1]])
                    self.posX = self.posX - vector_displacement[0]
                    self.posY = self.posY - vector_displacement[1]
                else:
                    self.endPosition = np.vstack([self.endPosition, [self.posX - vector_displacement[0], self.posY - vector_displacement[1]]])
                    self.posX = self.posX - vector_displacement[0]
                    self.posY = self.posY - vector_displacement[1]

            if self.endPosition is not None:
                if [self.posX, self.posY] in self.endPosition.tolist():
                    canMove = False
                    self.endPosition = np.vstack([self.endPosition, [self.posX - vector_displacement[0], self.posY - vector_displacement[1]]])
                    self.posX = self.posX - vector_displacement[0]
                    self.posY = self.posY - vector_displacement[1]


    def doDLA(self, L):

        self.L = L

        if (self.L % 2) == 0:  # If L is an even number
            raise ValueError('The length L of your grid has to be an odd number')

        canMove = True

        while(canMove):
            self.doParcour()
            if self.posY == 0 and self.posX == 0:
                canMove = False

        return self.endPosition

    def plotBrownianTree(self):

        plt.figure(1)

        plt.scatter(self.endPosition[:, 0], self.endPosition[:, 1], s=10, c=np.linspace(0, len(self.endPosition), len(self.endPosition)),
                    cmap='rainbow')
        plt.show()


if __name__ == '__main__':

    L = 50
    my_DLA = DLA()
    positions = my_DLA.doDLA(L+1)
    my_DLA.plotBrownianTree()

    # plt.figure(1)
    # plt.axvline(x=(-L /2), ymax=L/2, ymin= -L / 2)
    # plt.axvline(x=(L / 2), ymax=L / 2, ymin= -L / 2)
    # plt.axhline(y=(-L / 2), xmax=L / 2, xmin= -L / 2)
    # plt.axhline(y=(L / 2), xmax=L / 2, xmin= -L / 2)
    # plt.plot(positions[:, 0], positions[:, 1], 'o')
    # plt.show()