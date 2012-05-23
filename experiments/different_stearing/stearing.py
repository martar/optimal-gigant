'''
Here we see different stearing of the racer


'''

import pylab
from math import pi
from visual import vector
from skier import Skier
from simulation import SkierSimulation
import skier_with_air_resistance_force
from radius_processors import cutting_turns, falling_leaf, tightening_turns,circle




mi = 0.05 #waxed skis - typical value

alfa = pi/2
roh = 1.32 #kg*(m^(-3))

m = 60 #kg
C = 0.6  #drag coefficient, typical values (0.4 - 1)

A_A = 0.2 # m^2- medium position between upright and tucked
k2_A = 0.5 * C * roh * A_A

A_B = 0.16 # m^2- tucked position
k2_B = 0.5 * C * roh * A_B

k1 = 0.05 #imaginary value
x0 = vector(0,0)
v01 = vector(0,40)   #'''sqrt(2000)'''
v02 = vector(2,0)

kappa = 1/20.0
sim = SkierSimulation(distance=100, interval=0.001, solver=skier_with_air_resistance_force.solver, time_zoom=100)
s_A = Skier(mi, alfa, k1, k2_A, m, x0, v01, kappa)

s_B = Skier(mi, alfa, k1, k2_A, m, x0, v01, kappa)

s_C = Skier(mi, alfa, k1, k2_A, m, x0, v01, kappa)
   
# set the appropriate steering
#s_A.radius_processor = falling_leaf
s_A.radius_processor = tightening_turns

s_B.radius_processor = cutting_turns

s_C.radius_processor = circle
    
#sim.add_racer(s_A)
sim.add_racer(s_C)
#sim.add_racer(s_C)

sim.run()

pylab.plot(sim.timeline,s_C.positions) 

pylab.xlabel("time in seconds")
pylab.ylabel("distance in meters")
pylab.grid(True)
pylab.show()