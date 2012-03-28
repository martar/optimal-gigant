from simulation import SkierSimulation,skier_with_air_resistance_force
from math import pi

'''
This experiment checks the behaviour of the skiers with different air drag
'''

sim = SkierSimulation()
sim.add_racer(0.1, pi/3, 0.3, 70, skier_with_air_resistance_force.solver)
sim.add_racer(0.1, pi/3, 0.1, 70, skier_with_air_resistance_force.solver)
sim.run()
