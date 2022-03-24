from randomwalk import walkingDot
import time

start = time.time()
my_walkingDot = walkingDot()
my_walkingDot.doTheWalk(20000, 500, 101)
my_walkingDot.plotMeanDisplacementHist()
end = time.time()
print(end - start)
my_walkingDot.animateTheWalk(10)
