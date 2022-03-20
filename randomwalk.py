import numpy as np
import matplotlib.pyplot as plt
import random as rd

class walkingDot:
    def __init__(self):
        self.n = None # Number of dot
        self.N = None  # Number of step to take
        self.L = None  # Grid dimension in wich the dot can walk
        self.posX = None # Array for the X position of each dot at each step
        self.posY = None # Array for the Y position of each dot at each step

    def doTheWalk(self, n:int, N:int, L:int):
        self.n = n
        self.N = N
        self.L = L
        self.posX = np.zeros((self.N + 1, self.n))
        self.posY = np.zeros((self.N + 1, self.n))

        if (self.L % 2) == 0: # If L is an even number
            raise ValueError('The length L of your grid has to be an odd number')

        for j in range(0, self.n):
            for i in range(1, self.N + 1):
                a = True
                while (a):
                    dir = rd.randint(1, 4)
                    if dir == 1 and self.posY[i, j] < (self.L - 1) / 2:
                        self.posY[i:, j] += 1
                        a = False
                    elif dir == 2 and self.posX[i, j] < (self.L - 1) / 2:
                        self.posX[i:, j] += 1
                        a = False
                    elif dir == 3 and self.posY[i, j] > -(self.L - 1) / 2:
                        self.posY[i:, j] += -1
                        a = False
                    elif dir == 4 and self.posX[i, j] > -(self.L - 1) / 2:
                        self.posX[i:, j] += -1
                        a = False
        # return self.posX, self.posY

    def getPosition(self, stepNumber):

        if np.all((self.posX == 0)) is True and np.all((self.posY == 0)) is True:
            raise ValueError('You have to doTheWalk before you can get the position of your dots')
        elif stepNumber > self.N:
            raise ValueError('Step number out of range. Chose a step number between 0 and N')

        posX_atStepNumber = self.posX[stepNumber, :]
        posY_atStepNumber = self.posY[stepNumber, :]

        return posX_atStepNumber, posY_atStepNumber

    def getMeanDisplacement(self):

        finalpos_X, finalpos_Y = self.getPosition(self.N)
        meanDisplacement = np.sqrt(finalpos_X**2 + finalpos_Y**2)

        return meanDisplacement

    # def getSTD(self):

    def plotMeanDisplacementHist(self):
        meanDisplacement = self.getMeanDisplacement()
        plt.figure(1)
        plt.title('Mean displacement distribution of '+str(self.n)+' dots for '+str(self.N)+' steps \n in a '
                  +str(self.L)+'x'+str(self.L)+' grid.')

        plt.hist(meanDisplacement, bins='auto', density=True, facecolor='g')
        plt.xlabel('Mean displacement [-]')
        plt.ylabel('')
        plt.show()

    # def animateTheWalk(self, frame):



# if __name__ == '__main__':
#     my_walkingDot = walkingDot()
#     my_walkingDot.doTheWalk(10000, 200, 101)
#     my_walkingDot.plotMeanDisplacementHist()
#     my_walkingDot2 = walkingDot()
#     my_walkingDot2.doTheWalk(10000, 200, 51)
#     my_walkingDot2.plotMeanDisplacementHist()