from math import pi
import skier_with_air_resistance_force as skier
import numpy as np
import pylab as p

mi = 0.2
alfa = pi/3.0
k=0.1
t = np.linspace(0, 5, 21)
params = [alfa,mi,k]

result = skier.solver( t, params)

result2 = skier.solver( t, [alfa/2,mi,k])

result3 = skier.solver( t, [alfa,mi,0.01])

x = result[:, 0]
v = result[:, 1]

x2 = result2[:, 0]
x3 = result3[:, 0]


p.plot(t,x, t,v, t, x2, t, x3)
p.legend(('x', 'v', 'x2', 'x3'))
p.grid(True)
p.show()   