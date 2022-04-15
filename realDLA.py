import numpy as np
import matplotlib.pyplot as plt
import random as rd

class DLA:

    def __init__(self):

        self.possible_displacement = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
        self.L = None
        self.newL = 0
        self.posX = 0  # Array for the X position of each dot at each step
        self.posY = 0  # Array for the Y position of each dot at each step
        self.endPosition = np.array([[0, 0]])

    def displacement(self, possible_displacement):

        rng = np.random.default_rng()

        return rng.choice(possible_displacement).T

    def checkLimitBreak(self, posX, posY):

        boolX = np.where((-1*(self.L - 1) / 2 <= posX) & (posX <= (self.L - 1) / 2), True, False)
        boolY = np.where((-1*(self.L - 1) / 2 <= posY) & (posY <= (self.L - 1) / 2), True, False)

        return boolX, boolY

    def getStartingPoint(self):

        if np.size(self.endPosition) == 2:
            newL = 1
            position = self.displacement(self.possible_displacement)
            return position[0], position[1], newL

        else:
            newL = np.amax(np.abs(self.endPosition)) + 1
            newTheta = rd.randint(0, 359)
            return int(newL * np.cos(np.radians(newTheta))), int(newL * np.sin(np.radians(newTheta))), newL


    def doParcour(self):

        self.posX, self.posY, self.newL = self.getStartingPoint()

        canMove = True

        while(canMove):

            vector_displacement = self.displacement(self.possible_displacement)
            self.posX += vector_displacement[0]
            self.posY += vector_displacement[1]
            limitSate = self.checkLimitBreak(self.posX, self.posY)

            if (limitSate[0] == False or limitSate[1] == False) == True :
                canMove = False

            if [self.posX, self.posY] in self.endPosition.tolist():
                canMove = False
                self.endPosition = np.vstack([self.endPosition, [self.posX - vector_displacement[0], self.posY - vector_displacement[1]]])

            if int(np.sqrt(self.posY**2 + self.posX**2)) > self.newL*2:
                canMove = False


    def doDLA(self, L):

        self.L = L

        if (self.L % 2) == 0:  # If L is an even number
            raise ValueError('The length L of your grid has to be an odd number')

        canMove = True

        while(canMove):
            percent = (1 - (self.newL/((self.L-1)/3)))*100
            print('{:.0f}% left'.format(percent))
            self.doParcour()
            if self.newL > (self.L - 1) / 3:
                canMove = False
                print('Done')

        return self.endPosition

    def plotBrownianTree(self):

        L = self.L - 1
        plt.figure(1)
        plt.style.use('dark_background')
        plt.title('Carrée de '+str(self.L)+'x'+str(self.L))
        plt.axvline(x=(-L / 2), ymax=0.05, ymin=0.95, color='black')
        plt.axvline(x=(L / 2), ymax=0.05, ymin=0.95, color='black')
        plt.axhline(y=(-L / 2), xmax=0.05, xmin=0.95, color='black')
        plt.axhline(y=(L / 2), xmax=0.05, xmin=0.95, color='black')
        orig_map = plt.cm.get_cmap('rainbow')
        reversed_map = orig_map.reversed()
        c = np.linspace(0, len(self.endPosition), len(self.endPosition))
        plt.scatter(self.endPosition[:, 0], self.endPosition[:, 1], s=8, c=c[::-1],
                    cmap=reversed_map)
        plt.colorbar(label='Âge [itération]')
        plt.show()


if __name__ == '__main__':

    my_DLA = DLA()
    positions = my_DLA.doDLA(101)
    my_DLA.plotBrownianTree()