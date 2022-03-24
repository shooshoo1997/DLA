import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random as rd
import time
import numpy.ma as ma




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
        
        def checkposition(v_limite):  # utiliser des masked array ? np.where?
            check_y = np.abs(self.posY[i, :]) < (self.L - 1) / 2  # en haut ou en bas
            v_limite = v_limite & check_y
            check_x = np.abs(self.posX[i, :]) < (self.L - 1) / 2  # droite ou gauche
            v_limite = v_limite & check_x
            return v_limite

        possible_displacement = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
        rng = np.random.default_rng()
        def displacement():  # fonction génératrice à la place ?
            return rng.choice(possible_displacement, size=self.n, replace=True).T

        vector_limite = np.full((1, self.n), True)
        for i in range(1, self.N + 1):
            vector_displacement = displacement()
            self.posX[i, :] = np.where(np.abs(self.posX[i, :]) > (self.L - 1) / 2, self.posX[i, :], self.posX[i - 1, :] + vector_displacement[0])
            self.posY[i, :] = np.where(np.abs(self.posY[i, :]) > (self.L - 1) / 2, self.posY[i, :], self.posY[i - 1, :] + vector_displacement[1])

            vector_limite = checkposition(vector_limite)
            if np.sum(vector_limite) == 0:
                break

        
    def getPosition(self, stepNumber):

        if np.all((self.posX == 0)) is True and np.all((self.posY == 0)) is True:
            raise ValueError('You have to doTheWalk before you can get the position of your dots')
        elif stepNumber > self.N:
            raise ValueError('Step number out of range. Chose a step number between 0 and N')

        posX_atStepNumber = self.posX[stepNumber, :]
        posY_atStepNumber = self.posY[stepNumber, :]

        return posX_atStepNumber, posY_atStepNumber

    def getAllPositionSinceStart(self, stepNumber):

        if stepNumber > self.N:
            raise ValueError('Step number out of range. Chose a step number between 0 and N')

        posX_sinceStart = self.posX[:stepNumber, :]
        posY_sinceStart = self.posY[:stepNumber, :]
        posOfAllPoints = np.vstack(([posX_sinceStart.T], [posY_sinceStart.T])).T

        return  posOfAllPoints

    def getMeanDisplacement(self):

        finalpos_X, finalpos_Y = self.getPosition(self.N)
        meanDisplacement = np.sqrt(finalpos_X**2 + finalpos_Y**2)

        return meanDisplacement

    def getMeanOfAllDisplacement(self):

        return np.mean(self.getMeanDisplacement())

    def getSTDOfAllDisplacement(self):

        return np.std(self.getMeanOfAllDisplacement())

    def plotMeanDisplacementHist(self):

        meanDisplacement = self.getMeanDisplacement()
        meanOfAll = np.mean(meanDisplacement)
        stdOfAll = np.std(meanDisplacement)
        plt.clf()
        plt.figure(1)
        plt.title('Mean displacement distribution of '+str(self.n)+' dots for '+str(self.N)+' steps \n in a '
                  +str(self.L)+'x'+str(self.L)+' grid.')

        plt.hist(meanDisplacement, bins='auto', density=True, facecolor='g')
        plt.xlabel('Mean displacement [-]')
        plt.ylabel('')
        plt.legend(['$\mu = $'+'%.2f'%meanOfAll+', $\sigma =$'+'%.2f'%stdOfAll])
        plt.show()

    def animateT(self, N):

        plt.clf()
        plt.xlim(-(self.L - 1) / 2, (self.L - 1) / 2)
        plt.ylim(-(self.L - 1) / 2, (self.L - 1) / 2)
        vstack = self.getAllPositionSinceStart(N)
        tree = plt.plot(vstack[0:N][:, 0:self.numberOfDots, 0], vstack[0:N][:, 0:self.numberOfDots, 1])
        return tree

    def animateTheWalk(self, numberOfDots):
        self.numberOfDots = numberOfDots
        fig = plt.figure(1)
        ani = FuncAnimation(fig, self.animateT, self.N, interval=1)
        plt.show()


if __name__ == '__main__':
    # my_walkingDot = walkingDot()
    # my_walkingDot.doTheWalk(20000, 500, 101)
    # my_walkingDot.plotMeanDisplacementHist()

    my_walkingDot2 = walkingDot()
    my_walkingDot2.doTheWalk(100, 250, 101)  # points, nombre de pas, nombre de pixel dans la boîte
    my_walkingDot2.plotMeanDisplacementHist()
    my_walkingDot2.animateTheWalk(2)
