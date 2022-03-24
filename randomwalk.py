import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random as rd
import time
import numpy.ma as ma
from beartype import beartype
import matplotlib.ticker as ticker



class WalkingDot:
    
    def __init__(self):
        plt.close('all')
        self.n = None # Number of dot
        self.N = None  # Number of step to take
        self.L = None  # Grid dimension in wich the dot can walk
        self.posX = None # Array for the X position of each dot at each step
        self.posY = None # Array for the Y position of each dot at each step

        
    def checkposition(self, v_limite, i):  # utiliser des masked array ? np.where?
        check_y = np.abs(self.posY[i, :]) < (self.L - 1) / 2  # en haut ou en bas
        v_limite = v_limite & check_y
        check_x = np.abs(self.posX[i, :]) < (self.L - 1) / 2  # droite ou gauche
        v_limite = v_limite & check_x
        return v_limite
    
    def displacement(self, possible_displacement):  # fonction génératrice à la place ?
        rng = np.random.default_rng()
        return rng.choice(possible_displacement, size=self.n, replace=True).T
    
    @beartype # Vérifie les types d'arguments, souvlève un exception si type est pas bon
    def doTheWalk(self, n:int, N:int, L:int):

        self.n = n
        self.N = N
        self.L = L
        self.posX = np.zeros((self.N + 1, self.n))
        self.posY = np.zeros((self.N + 1, self.n))
        
        if (self.L % 2) == 0: # If L is an even number
            raise ValueError('The length L of your grid has to be an odd number')
        
        possible_displacement = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
        
        
        vector_limite = np.full((1, self.n), True)
        for i in range(1, self.N + 1):
            vector_displacement = self. displacement(possible_displacement)
            self.posX[i, :] = np.where(np.abs(self.posX[i, :]) > (self.L - 1) / 2, self.posX[i, :], self.posX[i - 1, :] + vector_displacement[0])
            self.posY[i, :] = np.where(np.abs(self.posY[i, :]) > (self.L - 1) / 2, self.posY[i, :], self.posY[i - 1, :] + vector_displacement[1])

            vector_limite = self.checkposition(vector_limite, i)
            if np.sum(vector_limite) == 0:
                break

        
    def getPosition(self, stepNumber):

        if isinstance(self.posX, type(None))  or(np.all((self.posX == 0)) is True and np.all((self.posY == 0)) is True):
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

    def getDisplacement(self):

        finalpos_X, finalpos_Y = self.getPosition(self.N)
        Displacement = np.sqrt(finalpos_X**2 + finalpos_Y**2)
        sigma = np.mean([np.std(finalpos_X), np.std(finalpos_Y)])
        return (Displacement, sigma)


    def getMeanOfAllDisplacement(self):

        return np.mean(self.getDisplacement()[0])

    def getSTDOfAllDisplacement(self):

        return np.std(self.getDisplacement()[0])

    def plotDisplacementHist(self):

        Displacement, sigma = self.getDisplacement()
        x = np.linspace(0,1.05*np.max(Displacement), 1000)
        Rayleigh_dist = x/(sigma**2)*np.exp(-x**2/(2*sigma**2))
        Rayleigh_mean = sigma*np.sqrt(np.pi/2)
        Rayleigh_std = np.sqrt((4-np.pi)/2)*sigma
        meanOfAll = self.getMeanOfAllDisplacement()
        stdOfAll = self.getSTDOfAllDisplacement()
        plt.clf()
        plt.figure(1)
        plt.title('Displacement distribution of '+str(self.n)+' dots for '+str(self.N)+' steps \n in a '
                  +str(self.L)+'x'+str(self.L)+' grid.')

        plt.hist(Displacement, bins='sturges', density=True, facecolor='g')
        plt.plot(x,Rayleigh_dist)
        plt.xlabel('Displacement [-]')
        plt.ylabel('Normalized frequency')
        plt.legend(['$Rayleigh: \mu = $'+'%.2f'%Rayleigh_mean+', $\sigma =$'+'%.2f'%Rayleigh_std,\
                    '$Data: \mu = $'+'%.2f'%meanOfAll+', $\sigma =$'+'%.2f'%stdOfAll])
        plt.show()

    def animateT(self, N):
        tick_spacing = 10
        plt.clf()
        plt.xlim(-(self.L - 1) / 2, (self.L - 1) / 2)
        plt.ylim(-(self.L - 1) / 2, (self.L - 1) / 2)
        plt.xlabel('X axis [-]')
        plt.ylabel('Y axis [-]')
        plt.title('Random walk of '+ str(self.numberOfDots)+' dots' +' for '+ str(self.N) + ' steps')
        plt.grid()
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
        plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
        vstack = self.getAllPositionSinceStart(self.nsteps)
        plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.jet(np.linspace(0, 1, self.numberOfDots))))
        tree = plt.plot(vstack[N-1:N][:, 0:self.numberOfDots, 0], vstack[N-1:N][:, 0:self.numberOfDots, 1],'o',\
                        vstack[0:N][:, 0:self.numberOfDots, 0], vstack[0:N][:, 0:self.numberOfDots, 1])
            
        return tree
    
    def animateTheWalk(self, numberOfDots, nsteps):
        self.nsteps = nsteps
        self.numberOfDots = numberOfDots
        fig = plt.figure(2)
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.clf()
        anim = FuncAnimation(fig, self.animateT, nsteps, interval=100, repeat=False)
        plt.show()
        return anim


if __name__ == '__main__':
    # my_walkingDot = walkingDot()
    # my_walkingDot.doTheWalk(20000, 500, 101)
    # my_walkingDot.plotMeanDisplacementHist()

    my_walkingDot2 = WalkingDot()
    my_walkingDot2.doTheWalk(1000, 500, 201)  # points, nombre de pas, nombre de pixel dans la boîte
    my_walkingDot2.plotDisplacementHist()
    anim = my_walkingDot2.animateTheWalk(10, 200)