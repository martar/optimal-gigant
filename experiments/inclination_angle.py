from simulation import SkierSimulation,skier_with_air_resistance_force
from math import pi

'''
This experiment checks the behaviour of the skiers with different inclination angle
'''

sim = SkierSimulation(end_time=4)
# pi/3 = 60 degrees
sim.add_racer(0.2, pi/3, 0.2, 70, skier_with_air_resistance_force.solver)
# pi/6 = 30 degrees
sim.add_racer(0.2, pi/6, 0.2, 70, skier_with_air_resistance_force.solver)
sim.run()
