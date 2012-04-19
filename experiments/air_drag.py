from simulation import SkierSimulation, Skier, skier_with_air_resistance_force
from math import pi
import pylab

'''
Harenda - 210 m / 600m -> alfa = atan(210/600) = ~~~21 degrees
This experiment checks the behaviour of the skiers with different air drag
'''

mi = 0.05 #waxed skis - typical value
alfa= 0.33667 #Harenda
roh = 1.32 #kg*(m^(-3))

m = 60 #kg
C = 0.6  #drag coficiant, typical values (0.4 - 1)

A_A = 0.2 # m^2- medium position between upright and tucked
k2_A = 0.5 * C * roh * A_A

A_B = 0.16 # m^2- tucked position
k2_B = 0.5 * C * roh * A_B

k1 = 0.05 #imaginary value
x0 = 0
v0 = 0
sim = SkierSimulation(distance=600, solver=skier_with_air_resistance_force.solver, time_zoom=100)
s_A = Skier(mi, alfa, k1, k2_A, m, x0, v0)
s_B = Skier(mi, alfa, k1, k2_B, m, x0, v0)
sim.add_racer(s_A)
sim.add_racer(s_B)
sim.run()
print 'Time of A %f, Time of B is %f' %(s_A.result,s_B.result)
print 'Time difference between A and B is %f seconds' %(s_A.result - s_B.result)
pylab.plot(sim.timeline,s_A.positions, 
           sim.timeline,s_B.positions,)
pylab.legend(('medium position', 'tucked position'), loc='lower right')
pylab.xlabel("time in seconds")
pylab.ylabel("distance in meters")
pylab.grid(True)
pylab.show()
