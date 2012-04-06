from simulation import SkierSimulation, Skier, skier_with_air_resistance_force
from numpy import tan, pi
import pylab

'''
This experiment checks the impact of the mass on slopes 
with different steepnes. How does the mass differance infulace the
performace on very gentle slope and how one very steep one?

Harenda - 210 m / 600m -> alfa = tan(210/600) = ~~~21 degrees
Polczakowka - 130 m / 650 m -> alfa = tan(130/650) = ~~~11.6 degrees
Kotelnica - 200 m / 1350 m -> alfa = tan(200/1350) = ~~~ 8.5 degress
'''
mi = 0.05 #waxed skis - typical value
roh = 1.32 #kg*(m^(-3))
C = 0.6  #drag coficiant, typical values (0.4 - 1)
A= 0.2 # m^2- medium position between upright and tucked
k2 = 0.5 * C * roh * A
k1 = 0.05 #imaginary value
x0 = 0
v0 = 0

alfa_HARENDA= 0.2027
alfa_KOTELNICA= 0.1492

m_A = 60 #kg
m_B = 100

sim = SkierSimulation(solver=skier_with_air_resistance_force.solver, time_zoom=1000)
s_A = Skier(mi, alfa_HARENDA, k1, k2, m_A, x0, v0)
s_B = Skier(mi, alfa_HARENDA, k1, k2, m_B, x0, v0)
s_A2 = Skier(mi, alfa_KOTELNICA, k1, k2, m_A, x0, v0)
s_B2 = Skier(mi, alfa_KOTELNICA, k1, k2, m_B, x0, v0)

sim.add_racer(s_A)
sim.add_racer(s_B)
sim.add_racer(s_A2)
sim.add_racer(s_B2)
sim.run()
print 'Time difference between A and B on steeper slope is %f seconds' %(s_A.result - s_B.result)
print 'Time difference between A and B on gentle slope is %f seconds' %(s_A2.result - s_B2.result)
pylab.plot(sim.timeline,s_A.positions, 
           sim.timeline,s_B.positions,
           sim.timeline,s_A2.positions,
           sim.timeline,s_B2.positions,)
pylab.legend(('60 kg skier steeper', '100 kg skier steeper',
             '60 kg skier gentle', '100 kg skier gentle'), loc='lower right')
pylab.xlabel("time in seconds")
pylab.ylabel("distance in meters")
pylab.grid(True)
pylab.show()