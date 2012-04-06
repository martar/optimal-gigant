from math import sin, cos
# standard acceleration of gravity
from scipy.constants import g
from scipy.integrate import odeint

'''
This module defines a first version of the skier-movement model. The model assumes
constant friction and air drag force that depends on velocity
'''


def _vectorfield(w, t, params):
    '''
    Right hand side of the differential equation.
    
    d2x/dt2 = g*sin(alfa) - mi*g*cos(alfa) - k1 * (dx/dt) / m - k2* (dx/dt)^2 /m 
    
     '''
    x, v = w
    alfa, mi, k1, k2, m  = params
    
    f = [v,                                     # dx/dt
         g*sin(alfa)-mi*g*cos(alfa)- k1/m*v -k2/m*v*v]    # dv/dt
    return f

def solver(t, x0, v0, alfa, mi, k1, k2, m, B=4):
    '''
    Solves the move equation. Move happens on an inclined plane with 
    rules of uniformly accelerated motion.
    Air resistance force is dependent with velocity, friction is constant.
    Arguments:
        x0: initial position 
        v0: initial velocity in m/s
        t: time - list of discrete time samples to be considered e.g. np.linspace(0, 5, 21)
        alfa: slope degree (degree between  B and C)
           |\     
           |  \
        A  |    \  C
           | alfa \
           |________\
               B   
        mi: coefficient of friction       
        k1: air drag factor
        k2: air drag 
        m : skier mass in kg
        B : boundary value (in m/s) from with air drag becomes 
                proportional to the square of the velocity.
    '''
    if v0 <= B:
        k2 = 0
    else:
        k1 = 0
    params = [alfa, mi, k1, k2, m]
    return odeint(_vectorfield, [x0, v0], t, args=(params,) ) 