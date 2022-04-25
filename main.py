import timeit


### RANDOM WALK ###

from randomwalk import WalkingDot

my_walkingDot = WalkingDot()

start = timeit.default_timer()

my_walkingDot.doTheWalk(100000, 500, 101)      # 100 000 billes, 500 pas, boite de 101x101

stop = timeit.default_timer()
minute = int((stop - start)/60)
seconde = (((stop - start)/60)%1)*60
print('Runtime: '+str(minute)+' minutes  {:.0f} secondes'.format(seconde))

my_walkingDot.plotXYHist()
my_walkingDot.plotDisplacementHist('gaussian') # Choix: "gaussian", "uniform"
my_walkingDot.animateTheWalk(10, 200)          # Animation 10 billes pour 200 pas


### DLA vesrion 1 ###

from simplifiedDLA import DLA as simpDLA

my_DLA = simpDLA()

start = timeit.default_timer()

positions = my_DLA.doDLA(101)                  # Boite de 101x101

stop = timeit.default_timer()
minute = int((stop - start)/60)
seconde = (((stop - start)/60)%1)*60
print('Runtime: '+str(minute)+' minutes  {:.0f} secondes'.format(seconde))

my_DLA.plotBrownianTree()


### DLA version 2 ###

from realDLA import DLA as trueDLA

my_DLA = trueDLA()

start = timeit.default_timer()

positions = my_DLA.doDLA(101)                  # Boite de 101x101

stop = timeit.default_timer()
minute = int((stop - start)/60)
seconde = (((stop - start)/60)%1)*60
print('Runtime: '+str(minute)+' minutes  {:.0f} secondes'.format(seconde))

my_DLA.plotBrownianTree()

