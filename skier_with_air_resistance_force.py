from math import sin, cos, acos, sqrt,asin
# standard acceleration of gravity
from scipy.constants.constants import g
from scipy.integrate import odeint
from visual import vector,mag

'''
This module defines a first version of the skier-movement model. The model assumes
constant friction and air drag force that depends on velocity
'''


def _vectorfield(w, t, params):
    '''
    Right hand side of the differential equation.
    
    d2x/dt2 = g*sin(alfa) - mi*g*cos(alfa) - k1 * (dx/dt) / m - k2* (dx/dt)^2 /m 
    
     '''
    x, v_len = w
    
    alfa, mi, k1, k2, m, prev_v, interval, v, R, beta  = params
    prev_v_len = mag(prev_v)
    prev_v_len = v_len
    #print beta

    f = [v_len,                                     # dx/dt
         g*sin(alfa)*sin(beta) + (v_len-prev_v_len)/interval 
         - mi*g*cos(alfa) - k1/m*v_len -k2/m*v_len*v_len]    # dv/dt
    return f

def _vectorfield2(w, t, params):
    '''
    Right hand side of the differential equation.
    
    d2x/dt2 = g*sin(alfa) - mi*g*cos(alfa) - k1 * (dx/dt) / m - k2* (dx/dt)^2 /m 
    
     '''
    x, v_len = w
    alfa, mi, k1, k2, m, prev_v, interval, v, R, beta  = params
    v_len = 0
    f = [v_len,                                     # dx/dt
         g*sin(alfa)*cos(beta) + v_len**2/R]    # dv/dt
    return f

def solver(t, x0, v0, alfa, mi, k1, k2, m, prev_v, R=10000, B=4):
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
    print v0,x0
    v0_length = mag(v0)
    if v0_length <= B:
        k2 = 0
    else:
        k1 = 0
    beta = asin(v0[1]/v0_length)
    #print v0,v0_length,beta
   
    params = [alfa, mi, k1, k2, m, prev_v, t[1]-t[0], v0, R, beta]
    x0_len = mag(x0)
    st = odeint(_vectorfield, [x0_len, v0_length], t, args=(params,) )
    norm = odeint(_vectorfield2, [x0_len, v0_length], t, args=(params,) )
    print "v_new",st[1],norm[1]
    
    
    
    return st, norm, beta