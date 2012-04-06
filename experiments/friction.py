from simulation import SkierSimulation, Skier, skier_with_air_resistance_force
from math import pi
import pylab

'''
This experiment checks the behaviour of the skiers with different friction
'''

mi_A = 0.05 #waxed skis - typical value
mi_B = 0.1

alfa= pi/12 #15` degrees
roh = 1.32 #kg*(m^(-3))

m = 60 #kg
C = 0.6  #drag coficiant, typical values (0.4 - 1)

A= 0.2 # m^2- medium position between upright and tucked
k2 = 0.5 * C * roh * A
k1 = 0.05 #imaginary value
x0 = 0
v0 = 0
sim = SkierSimulation(solver=skier_with_air_resistance_force.solver, time_zoom=100)
s_A = Skier(mi_A, alfa, k1, k2, m, x0, v0)
s_B = Skier(mi_B, alfa, k1, k2, m, x0, v0)
sim.add_racer(s_A)
sim.add_racer(s_B)
sim.run()
print 'Time difference between A and B is %f seconds' %(s_A.result - s_B.result)
pylab.plot(sim.timeline,s_A.positions, 
           sim.timeline,s_B.positions,)
pylab.legend(('lower frictin', 'higher friction'), loc='lower right')
pylab.xlabel("time in seconds")
pylab.ylabel("distance in meters")
pylab.grid(True)
pylab.show()