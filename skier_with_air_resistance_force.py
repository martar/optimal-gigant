from math import sin, cos
# standard acceleration of gravity
from scipy.constants import g
from scipy.integrate import odeint

'''
This module defines a first version of the skier-movement model. The model assumes
constant friction and air resistance force that depends on velocity

//TODO improve the comment
'''


def _vectorfield(w, t, params):
    '''
    Right hand side of the differential equation.
    
    d2x/dt2 = g*sin(alfa) - mi*g*cos(alfa) - k* (dx/dt)^2 /m 
    
     '''
    x, v = w
    alfa, mi, k, m  = params
    
    f = [v,                                     # dx/dt
         g*sin(alfa)-mi*g*cos(alfa)- k/m*v*v]    # dv/dt
    return f

def solver(t, params, w=[0,0]):
    '''
    Solves the move equation. Move happens on an inclined plane with 
    rules of uniformly accelerated motion.
    Air resistance force is dependent with velocity, friction is constant.
    Arguments:
        w: vector of initial conditions (for time = 0) w = [x, v]
            x: initial position (one dimension vector???)
            v: initial velocity in m/s
        t: time - list of discrete time samples to be considered e.g. np.linspace(0, 5, 21)
        params: vector of the parameters params = (alfa, mi, k, m):
            alfa: slope degree (degree between  B and C)
               |\     
               |  \
            A  |    \  C
               | alfa \
               |________\
                   B   
            mi: coefficient of friction       
            k: resistance factor
            m: skier mass in kg
    '''
    return odeint(_vectorfield, w, t, args=(params,) ) 