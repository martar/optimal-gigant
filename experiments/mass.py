from simulation import SkierSimulation,skier_with_air_resistance_force
from math import pi

'''
This experiment checks the behaviour of the skiers with different masses
'''

sim = SkierSimulation(end_time=3)
sim.add_racer(0.2, pi/3, 0.1, 60, skier_with_air_resistance_force.solver)
sim.add_racer(0.2, pi/3, 0.1, 100, skier_with_air_resistance_force.solver)
sim.run()
