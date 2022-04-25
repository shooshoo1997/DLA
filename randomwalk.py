import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from beartype import beartype
import matplotlib.ticker as ticker


class WalkingDot:

    def __init__(self):
        plt.close('all')
        self.n = None  # Number of dot
        self.N = None  # Number of step to take
        self.L = None  # Grid dimension in wich the dot can walk
        self.posX = None  # Array for the X position of each dot at each step
        self.posY = None  # Array for the Y position of each dot at each step


    def displacement(self, possible_displacement):
        rng = np.random.default_rng()
        return rng.choice(possible_displacement, size=self.n, replace=True).T

    @beartype
    def doTheWalk(self, n: int, N: int, L: int):

        self.n = n
        self.N = N
        self.L = L
        self.posX = np.zeros((self.N + 1, self.n))
        self.posY = np.zeros((self.N + 1, self.n))

        if (self.L % 2) == 0:
            raise ValueError('The length L of your grid has to be an odd number')

        self.possible_displacement = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])

        for i in range(1, self.N + 1):
            vector_displacement = self.displacement(self.possible_displacement)
            self.posX[i, :] = self.posX[i - 1, :] + vector_displacement[0]
            self.posY[i, :] = self.posY[i - 1, :] + vector_displacement[1]
            self.posX[i, :] = np.where((-1*(self.L - 1) / 2 <= self.posX[i, :]) & (self.posX[i, :] <= (self.L - 1) / 2), self.posX[i, :],
                                       self.posX[i-1, :])
            self.posY[i, :] = np.where((-1*(self.L - 1) / 2 <= self.posY[i, :]) & (self.posY[i, :] <= (self.L - 1) / 2), self.posY[i, :],
                                       self.posY[i-1, :])


    def getPosition(self, stepNumber):

        if isinstance(self.posX, type(None)) or (np.all((self.posX == 0)) is True and np.all((self.posY == 0)) is True):
            raise ValueError('You have to doTheWalk before you can get the position of your dots')
        elif stepNumber > self.N:
            raise ValueError('Step number out of range. Chose a step number between 0 and N')

        posX_atStepNumber = self.posX[stepNumber, :]
        posY_atStepNumber = self.posY[stepNumber, :]

        return posX_atStepNumber, posY_atStepNumber

    def getAllPositionSinceStart(self, stepNumber, numberOfDots):

        if stepNumber > self.N:
            raise ValueError('Step number out of range. Chose a step number between 0 and N')

        posX_sinceStart = self.posX[:stepNumber, 0:numberOfDots]
        posY_sinceStart = self.posY[:stepNumber, 0:numberOfDots]
        posOfAllPoints = np.vstack(([posX_sinceStart.T], [posY_sinceStart.T])).T

        return posOfAllPoints

    def getDisplacement(self):

        finalpos_X, finalpos_Y = self.getPosition(self.N)
        Displacement = np.sqrt(finalpos_X ** 2 + finalpos_Y ** 2)
        sigma = np.mean([np.std(finalpos_X), np.std(finalpos_Y)])
        return (Displacement, sigma)

    def getMeanOfAllDisplacement(self):

        return np.mean(self.getDisplacement()[0])

    def getSTDOfAllDisplacement(self):

        return np.std(self.getDisplacement()[0])

    def plotDisplacementHist(self, methode:str):

        if methode == 'gaussian':

            Displacement, sigma = self.getDisplacement()
            x = np.linspace(0, 1.05 * np.max(Displacement), 1000)
            sigmaTheo = np.sqrt(self.N / 2)
            Rayleigh_dist = x / (sigmaTheo ** 2) * np.exp(-x ** 2 / (2 * sigmaTheo ** 2))
            Rayleigh_mean = sigmaTheo * np.sqrt(np.pi / 2)
            Rayleigh_std = np.sqrt((4 - np.pi) / 2) * sigmaTheo
            meanOfAll = self.getMeanOfAllDisplacement()
            stdOfAll = self.getSTDOfAllDisplacement()

            plt.figure()
            plt.title('Displacement distribution of ' + str(self.n) + ' dots for ' + str(self.N) + ' steps \n in a '
                      + str(self.L) + 'x' + str(self.L) + ' grid.')

            plt.hist(Displacement, bins='sturges', density=True, facecolor='g')
            plt.plot(x, Rayleigh_dist)
            plt.xlabel('Displacement [-]')
            plt.ylabel('Normalized frequency')
            plt.legend(['$Rayleigh: \mu = $' + '%.2f' % Rayleigh_mean + ', $\sigma =$' + '%.2f' % Rayleigh_std,
                        '$Data: \mu = $' + '%.2f' % meanOfAll + ', $\sigma =$' + '%.2f' % stdOfAll])
            plt.show()

        elif methode == 'uniform':

            Displacement, sigma = self.getDisplacement()
            x = np.linspace(0, np.sqrt(2)*((self.L-1)/2), 1000)
            unif_dist = np.zeros((1, 1000))
            for i, j in enumerate(x):
                if 0 <= j < ((self.L-1)/2):
                    unif_dist[0, i] = (1/(((self.L-1)/2)**2))* (np.pi/2) * j
                elif ((self.L-1)/2) <= j <= np.sqrt(2)*((self.L-1)/2):
                    unif_dist[0, i] = (1 / (((self.L - 1) / 2) ** 2)) * (np.pi/2 - 2*np.arccos(((self.L-1)/2)/j)) * j

            norm_Factor = np.sum(unif_dist)
            theo_Dist = np.sum(x[np.newaxis] * unif_dist/norm_Factor)
            unif_mean = theo_Dist
            unif_std = np.sqrt(np.sum((x[np.newaxis] - theo_Dist)**2 * unif_dist/norm_Factor))
            meanOfAll = self.getMeanOfAllDisplacement()
            stdOfAll = self.getSTDOfAllDisplacement()

            plt.figure()
            plt.title('Displacement distribution of ' + str(self.n) + ' dots for ' + str(self.N) + ' steps \n in a '
                      + str(self.L) + 'x' + str(self.L) + ' grid.')

            plt.hist(Displacement, bins='sturges', density=True, facecolor='g')
            plt.plot(x[np.newaxis].T, unif_dist.T)
            plt.xlabel('Displacement [-]')
            plt.ylabel('Normalized frequency')
            plt.legend(['$Theorical: \mu = $' + '%.2f' % unif_mean + ', $\sigma =$' + '%.2f' % unif_std,
                        '$Data: \mu = $' + '%.2f' % meanOfAll + ', $\sigma =$' + '%.2f' % stdOfAll])
            plt.show()
        else:
            raise ValueError(methode + ' is not a valid method. Chose between gaussian and uniform.')

    def plotXYHist(self, methode:str):

        finalpos_X, finalpos_Y = self.getPosition(self.N)
        meanX = np.mean(finalpos_X)
        meanY = np.mean(finalpos_Y)
        sigmaX = np.std(finalpos_X)
        sigmaY = np.std(finalpos_Y)

        if methode == 'gaussian':
            x = np.linspace(1.05 * np.min(finalpos_X), 1.05 * np.max(finalpos_X), 5000)
            meanTheo = 0
            sigmaTheo = np.sqrt(self.N / 2)
            Gaussian_dist = 1 / np.sqrt(2 * np.pi * sigmaTheo ** 2) * np.exp(-x ** 2 / (2 * sigmaTheo ** 2))

            fig1, (ax1) = plt.subplots()
            fig2, (ax2) = plt.subplots()
            ax1.hist(finalpos_X, bins='sturges', density=True, facecolor='g',
                     label='$Data X: \mu = $' + '%.2f' % meanX + ', $\sigma =$' + '%.2f' % sigmaX)
            ax1.plot(x, Gaussian_dist, label='$Gaussian: \mu = $' + '%.2f' % meanTheo + ', $\sigma =$' + '%.2f' % sigmaTheo)
            ax2.hist(finalpos_X, bins='sturges', density=True, facecolor='r',
                     label='$Data Y: \mu = $' + '%.2f' % meanY + ', $\sigma =$' + '%.2f' % sigmaY)
            ax2.plot(x, Gaussian_dist, label='$Gaussian: \mu = $' + '%.2f' % meanTheo + ', $\sigma =$' + '%.2f' % sigmaTheo)
            ax1.set_ylabel('Normalized frequency [-]')
            ax1.set_xlabel("X position [-]")
            ax2.set_xlabel("Y position [-]")
            ax1.set_title('Distribution of the final position of the dots on the Xaxis')
            ax2.set_title('Distribution of the final position of the dots on the Y axis')
            fig1.legend()
            fig2.legend()
            plt.show()

        if methode == 'uniform':
            x = np.linspace(1.05 * np.min(finalpos_X), 1.05 * np.max(finalpos_X), 5000)
            meanTheo = 0
            sigmaTheo = np.sqrt(self.N / 2)
            sigmaTheo_unif = self.L/np.sqrt(12)
            unif_Theo = 1/self.L
            Gaussian_dist = 1 / np.sqrt(2 * np.pi * sigmaTheo ** 2) * np.exp(-x ** 2 / (2 * sigmaTheo ** 2))
            unif_dist = np.full((5000), unif_Theo)

            fig1, (ax1) = plt.subplots()
            fig2, (ax2) = plt.subplots()
            ax1.hist(finalpos_X, bins='auto', density=True, facecolor='g',
                     label='$Data X: \mu = $' + '%.2f' % meanX + ', $\sigma =$' + '%.2f' % sigmaX)
            ax1.plot(x, Gaussian_dist,
                     label='$Gaussian: \mu = $' + '%.2f' % meanTheo + ', $\sigma =$' + '%.2f' % sigmaTheo)
            ax1.plot(x, unif_dist,
                     label='$Uniforme: \mu = $' + '%.2f' % meanTheo + ', $\sigma =$' + '%.2f' % sigmaTheo_unif, color='black')
            ax2.hist(finalpos_X, bins='auto', density=True, facecolor='r',
                     label='$Data Y: \mu = $' + '%.2f' % meanY + ', $\sigma =$' + '%.2f' % sigmaY)
            ax2.plot(x, Gaussian_dist,
                     label='$Gaussian: \mu = $' + '%.2f' % meanTheo + ', $\sigma =$' + '%.2f' % sigmaTheo)
            ax2.plot(x, unif_dist,
                     label='$Uniforme: \mu = $' + '%.2f' % meanTheo + ', $\sigma =$' + '%.2f' % sigmaTheo_unif, color='black')
            ax1.set_ylabel('Normalized frequency [-]')
            ax1.set_xlabel("X position [-]")
            ax2.set_xlabel("Y position [-]")
            ax1.set_title('Distribution of the final position of the dots on the Xaxis')
            ax2.set_title('Distribution of the final position of the dots on the Y axis')
            fig1.legend()
            fig2.legend()
            plt.show()

    def animateT(self, N):

        tick_spacing = 10
        plt.clf()
        plt.xlim(-(self.L - 1) / 2 - 10, (self.L - 1) / 2 + 10)
        plt.ylim(-(self.L - 1) / 2 - 10, (self.L - 1) / 2 + 10)
        plt.axhline(y=(self.L - 1) / 2, color='red')
        plt.axhline(y=-(self.L - 1) / 2, color='red')
        plt.axvline(x=-(self.L - 1) / 2, color='red')
        plt.axvline(x=(self.L - 1) / 2, color='red')
        plt.xlabel('X axis [-]')
        plt.ylabel('Y axis [-]')
        plt.title('Random walk of ' + str(self.numberOfDots) + ' dots' + ' for ' + str(self.nsteps) + ' steps')
        plt.grid()
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
        plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
        vstack = self.getAllPositionSinceStart(self.nsteps, self.numberOfDots)
        plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.jet(np.linspace(0, 1, self.numberOfDots))))
        tree = plt.plot(vstack[N - 1:N][:, 0:self.numberOfDots, 0], vstack[N - 1:N][:, 0:self.numberOfDots, 1], 'o',
                        vstack[0:N][:, 0:self.numberOfDots, 0], vstack[0:N][:, 0:self.numberOfDots, 1])

        return tree

    @beartype
    def animateTheWalk(self, numberOfDots: int, nsteps: int):
        if nsteps > self.N:
            raise ValueError('The number of steps is bigger than the number of steps made by the dots')
        elif numberOfDots > self.n:
            raise ValueError('The number of animated dots is bigger than the number of total dots')

        self.nsteps = nsteps
        self.numberOfDots = numberOfDots
        fig = plt.figure()
        plt.clf()
        anim = FuncAnimation(fig, self.animateT, nsteps, interval=1, repeat=False)
        plt.show()
        return anim

if __name__ == '__main__':


    my_walkingDot = WalkingDot()
    my_walkingDot.doTheWalk(100000, 1, 51) # 100 000 billes, 500 pas, boite de 101x101
    my_walkingDot.plotXYHist('gaussian')
    my_walkingDot.plotDisplacementHist('gaussian')
    my_walkingDot.animateTheWalk(10, 200)      # animation de 10 billes pour 200 pas