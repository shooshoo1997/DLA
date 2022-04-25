import numpy as np
import matplotlib.pyplot as plt
import random as rd


class DLA:

    def __init__(self):

        self.possible_displacement = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
        self.L = None
        self.n = 1
        self.posX = 0  # Array for the X position of each dot at each step
        self.posY = 0  # Array for the Y position of each dot at each step
        self.endPosition = None
        self.listIter = []

    def displacement(self, possible_displacement):

        rng = np.random.default_rng()

        return rng.choice(possible_displacement).T

    def getMask(self, posX, posY):


        boolX_limit = np.where((-1 * (self.L - 1) / 2 <= posX) & (posX <= (self.L - 1) / 2), True, False)
        boolY_limit = np.where((-1 * (self.L - 1) / 2 <= posY) & (posY <= (self.L - 1) / 2), True, False)
        return boolX_limit, boolY_limit

    def doParcour(self):

        self.posX = 0
        self.posY = 0

        canMove = True

        while(canMove):
            vector_displacement = self.displacement(self.possible_displacement)
            displacement_X = vector_displacement[0]
            displacement_Y = vector_displacement[1]

            self.posX += displacement_X
            self.posY += displacement_Y

            limitSate = self.getMask(self.posX, self.posY)

            if (limitSate[0] == False or limitSate[1] == False) == True :
                canMove = False
                if self.endPosition is None:
                    self.endPosition = np.array([self.posX - vector_displacement[0], self.posY - vector_displacement[1]])
                    self.endPosition = self.endPosition[np.newaxis]
                    self.posX = self.posX - vector_displacement[0]
                    self.posY = self.posY - vector_displacement[1]
                else:
                    self.endPosition = np.vstack([self.endPosition, [self.posX - vector_displacement[0], self.posY - vector_displacement[1]]])
                    self.posX = self.posX - vector_displacement[0]
                    self.posY = self.posY - vector_displacement[1]

            elif self.endPosition is not None:
                pos = self.posX+self.posY*1j
                endPos = self.endPosition[:, 0] + self.endPosition[:, 1]*1j
                if np.in1d(pos, endPos):
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

            if self.posY**2 + self.posX**2 == 0:
                canMove = False

        return self.endPosition, self.listIter

    def plotBrownianTree(self):

        L = self.L - 1
        plt.figure(1)
        plt.title('Carrée de '+str(self.L)+'x'+str(self.L))
        plt.axvline(x=(-L / 2), ymax=0.05, ymin=0.95, color='black')
        plt.axvline(x=(L / 2), ymax=0.05, ymin=0.95, color='black')
        plt.axhline(y=(-L / 2), xmax=0.05, xmin=0.95, color='black')
        plt.axhline(y=(L / 2), xmax=0.05, xmin=0.95, color='black')
        orig_map = plt.cm.get_cmap('rainbow')
        reversed_map = orig_map.reversed()
        c = np.linspace(0, len(self.endPosition), len(self.endPosition))
        plt.scatter(self.endPosition[:, 0], self.endPosition[:, 1], s=10, c=c[::-1],
                    cmap=reversed_map)
        plt.colorbar(label='Âge [itération]')
        plt.show()



if __name__ == '__main__':

    my_DLA = DLA()
    positions = my_DLA.doDLA(101) # Simulation avec L = 101
    my_DLA.plotBrownianTree()