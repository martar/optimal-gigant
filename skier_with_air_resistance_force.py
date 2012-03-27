from math import sin, cos
# standard acceleration of gravity
from scipy.constants import g
from scipy.integrate import odeint

'''
This module defines a first version of the skier-movement model. The model assumes
constant friction and air resistance force that is a dependend on velocity

//TODO improve the comment
'''


def _vectorfield(w, t, params):
    '''
    Right hand side of the differential equasiton.
    //TODO write an equasion!!
     '''
    x, v = w
    alfa, mi,k  = params
    
    f = [v,                                     # dx/dt
         g*sin(alfa)-mi*g*cos(alfa)- k *v*v]    # dv/dt
    return f

def solver(t, params, w=[0,0]):
    '''
    Solves the move equasion. Move happens on an inclined plane with 
    rules of uniformly accelerated motion.
    Air resianace force is dependent with velosity, friction is constant.
    Arguments:
        w: vector of initial conditions (for time = 0) w = [x, v]
            x: initial position (one dimension vector???)
            v: initila velocity in m/s
        t: time - list of discrete time samples to be considered for ex. np.linspace(0, 5, 21)
        params: vector of the parameters params = (alfa, mi, k):
            alfa: slope degree (degree between  B and C)
               |\     
               |  \
            A  |    \  C
               | alfa \
               |________\
                   B   
            mi: coefficient of friction       
            k: resistance factor (with mass "inside")
    '''
    return odeint(_vectorfield, w, t, args=(params,) ) 