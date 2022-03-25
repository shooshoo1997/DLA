from randomwalk import WalkingDot
import time

start = time.time()
my_walkingDot = WalkingDot()
my_walkingDot.doTheWalk(100000, 1000, 101)  # points, nombre de pas, nombre de pixel dans la boîte
my_walkingDot.plotXYHist()
my_walkingDot.plotDisplacementHist()
end = time.time()
print(end - start)
anim = my_walkingDot.animateTheWalk(20, 200)
