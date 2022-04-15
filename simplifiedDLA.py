import numpy as np
import matplotlib.pyplot as plt
import random as rd


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

    def getStartingPoint(self):

        # startingPlane = rd.randint(0, 3)
        if self.endPosition is None:
            startingPlane = rd.randint(0, 3)
            alongPlane = rd.randint(-1*(self.L - 1)/2, (self.L - 1)/2)
            if startingPlane == 0:
                return alongPlane, (self.L - 1)/2, self.L
            elif startingPlane == 2:
                return alongPlane, -1*(self.L - 1)/2, self.L
            elif startingPlane == 1:
                return (self.L - 1)/2, alongPlane, self.L
            elif startingPlane == 3:
                return -1*(self.L - 1)/2, alongPlane, self.L
        elif np.size(self.endPosition) == 2:
            newL = np.max(np.abs(self.endPosition)) - 1
            # print(newL)
            newTheta = rd.randint(0, 359)
            return int(abs(newL) * np.cos(np.radians(newTheta))), int(abs(newL) * np.sin(np.radians(newTheta))), abs(newL)

        else:
            maxMatrice = np.amax(np.abs(self.endPosition), axis=1)
            newL = np.min(maxMatrice) - 1
            # print(newL)
            newTheta = rd.randint(0, 359)
            if newL < 0:
                return 0, 0
            else:
                return int(abs(newL) * np.cos(np.radians(newTheta))), int(abs(newL) * np.sin(np.radians(newTheta))), abs(newL)

    def doParcour(self):

        self.posX, self.posY, newL = self.getStartingPoint() # Cette section uncommented pour utiliser l'algo accéléré (spoiler: ne fonctionne pas vraiment)
        # self.posX = 0 # Cette section commented pour utiliser l'algo accéléré
        # self.posY = 0 # Cette section commented pour utiliser l'algo accéléré
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

            elif self.endPosition is not None:
                if [self.posX, self.posY] in self.endPosition.tolist():
                    canMove = False
                    self.endPosition = np.vstack([self.endPosition, [self.posX - vector_displacement[0], self.posY - vector_displacement[1]]])
                    self.posX = self.posX - vector_displacement[0]
                    self.posY = self.posY - vector_displacement[1]
            elif int(np.sqrt(self.posY**2 + self.posX**2)) < int(newL/2):
                canMove = False

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
        plt.scatter(self.endPosition[:, 0], self.endPosition[:, 1], s=10, c=c[::-1],
                    cmap=reversed_map)
        plt.colorbar(label='Âge [itération]')
        plt.show()



if __name__ == '__main__':

    my_DLA = DLA()
    positions = my_DLA.doDLA(21)
    my_DLA.plotBrownianTree()