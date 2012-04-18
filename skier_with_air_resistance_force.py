from math import sin, cos, acos, sqrt,asin
# standard acceleration of gravity
from scipy.constants.constants import g
from scipy.integrate import odeint
from visual import vector,mag

'''
This module defines a first version of the skier-movement model. The model assumes
constant friction and air drag force that depends on velocity
'''


def _vectorfieldx(w, t, params):
    '''
    Right hand side of the differential equation.
    
    d2x/dt2 = g*sin(alfa) - mi*g*cos(alfa) - k1 * (dx/dt) / m - k2* (dx/dt)^2 /m 
    
     '''
    x, v_len = w
    
    alfa, mi, k1, k2, m, v, ksi  = params
    #print beta

    vl = mag(v)
    if(vl==0):
        cosinus=0
        sinus=1
    else:
        cosinus = v[0]/vl
        sinus = v[1]/vl
    #print v_len,"x",sinus,cosinus
    
    f = [v_len,                                     # dx/dt
         v_len**2*sinus*ksi 
         - (mi*g*cos(alfa) + k1/m*v_len + k2/m*v_len**2)*cosinus]    # dv/dt
    return f

def _vectorfieldy(w, t, params):
    '''
    Right hand side of the differential equation.
    
    d2x/dt2 = g*sin(alfa) - mi*g*cos(alfa) - k1 * (dx/dt) / m - k2* (dx/dt)^2 /m 
    
     '''
    x, v_len = w
    alfa, mi, k1, k2, m, v, ksi  = params
    
    vl = mag(v)
    if(vl==0):
        cosinus=0
        sinus=1
    else:
        cosinus = v[0]/vl
        sinus = v[1]/vl
    #print v_len,"y",sinus,cosinus
    
    f = [v_len,                                     # dx/dt
         g*sin(alfa) - v_len**2*ksi*cosinus
         - (mi*g*cos(alfa) + k1/m*v_len + k2/m*v_len*v_len)*sinus]    # dv/dt
    return f

def solver(t, x0, v0, alfa, mi, k1, k2, m, ksi=5, B=4):
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
    #print "x,v:",x0,v0
    v0_length = mag(v0)
    if v0_length <= B:
        k2 = 0
    else:
        k1 = 0
    #beta = asin(v0[1]/v0_length)
    #print v0,v0_length,beta
    #print ksi
    params = [alfa, mi, k1, k2, m, v0, ksi]
    x0_len = mag(x0)
    x = odeint(_vectorfieldx, [x0[0], v0[0]], t, args=(params,) )
    y = odeint(_vectorfieldy, [x0[1], v0[1]], t, args=(params,) )
    ''''x = odeint(_vectorfieldx, [x0_len, v0_length], t, args=(params,) )
    y = odeint(_vectorfieldy, [x0_len, v0_length], t, args=(params,) )'''
    print "x\t\tv\t\t\n",x[1],"\n",y[1]
    
    return x, y