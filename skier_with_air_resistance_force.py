from math import sin, cos
# standard acceleration of gravity
from scipy.constants.constants import g
from scipy.integrate import odeint
from visual import mag

'''
This module defines a second version of the skier-movement model. The model assumes
constant friction and air drag force that depends on velocity. Additionally we can set 
the curvature and make the skier turn. 
'''


def _vectorfieldx(w, t, params):
    '''
    Right hand side of the differential equation in x plane.
    
    d2x/dt2 = v**2*sinus(beta)*ksi - ( mi*g*cos(alfa) + k1*(dx/dt)/m - k2*(dx/dt)^2/m )*cos(beta) 
    
     '''
    _, vx = w
    
    alfa, mi, k1, k2, m, vl, ksi, cosinus, sinus  = params
    
    f = [vx,                                     # dx/dt
         vl**2*sinus*ksi 
         - (mi*g*cos(alfa) + k1/m*vl + k2/m*vl**2)*cosinus]    # dv/dt
    return f

def _vectorfieldy(w, t, params):
    '''
    Right hand side of the differential equation in y plane.
    
    d2x/dt2 = g*sin(alfa) - v**2*cos(beta)*ksi - ( mi*g*cos(alfa) + k1*(dx/dt)/m - k2*(dx/dt)^2/m )*sin(beta) 
    
     '''
    _, vy = w
    alfa, mi, k1, k2, m, vl, ksi, cosinus, sinus  = params
    
    
    f = [vy,                                     # dx/dt
         g*sin(alfa) - vl**2*ksi*cosinus
         - (mi*g*cos(alfa) + k1/m*vl + k2/m*vl**2)*sinus]    # dv/dt
    return f

def solver(t, x0, v0, alfa, mi, k1, k2, m, ksi=1/20.0, B=4):
    '''
    Solves the move equation. Move happens on an inclined plane with 
    rules of uniformly accelerated motion.
    Air resistance force is dependent with velocity, friction is constant.
    Arguments:
        x0: initial position - vector
        v0: initial velocity in m/s - vector
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
        ksi: curvature - reciprocal of the radius (positive makes right turn)
        B : boundary value (in m/s) from with air drag becomes 
                proportional to the square of the velocity.
    '''

    v0_length = mag(v0)
    if v0_length <= B:
        k2 = 0
    else:
        k1 = 0

    #find cos and sin(beta) from velocity vector 
    #where beta is the angle between x plane and velocity vector
    if(v0_length==0):
        cosinus=0.0
        sinus=1.0
    else:
        cosinus =  v0[0]/v0_length
        sinus = v0[1]/v0_length
    
    params = [alfa, mi, k1, k2, m, v0_length, ksi, cosinus, sinus]
    
    x0_len = mag(x0)
    x = odeint(_vectorfieldx, [x0[0], v0[0]], t, args=(params,) )
    y = odeint(_vectorfieldy, [x0[1], v0[1]], t, args=(params,) )
    #print "x\t\tv\t\t\n",x[1],"\n",y[1],"\t",t
    
    '''
    if abs(x[1][0])<0.00001: x[1][0]=0
    if abs(x[1][1])<0.00001: x[1][1]=0
    if abs(y[1][0])<0.00001: y[1][0]=0
    if abs(y[1][1])<0.00001: y[1][1]=0
    '''
    return x, y