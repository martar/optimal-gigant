from math import sin, cos
# standard acceleration of gravity
from scipy.constants.constants import g
from scipy.integrate import odeint
from numpy import sign
from visual import mag

'''
This module defines a second version of the skier-movement model. The model assumes
constant friction and air drag force that depends on velocity. Additionally we can set 
the curvature and make the skier turn. 
'''


def _vectorfield(w, t, params):
    '''
    Right hand side of the differential equation in x plane.
    
    d2x/dt2 = v**2*sinus(beta)*kappa - ( mi*g*cos(alfa) + k1*(dx/dt)/m - k2*(dx/dt)^2/m )*cos(beta) 
    
     '''
    _,_, vx, vy  = w
    
    alfa, mi, k1, k2, m, kappa, cosinus, sinus  = params
    vl = mag((vx,vy))
    
    f_r = vl**2*abs(kappa) + sign(kappa)*g*sin(alfa)*cosinus
    if f_r < 0:
        f_r = sign(kappa)*g*sin(alfa)*cosinus
        #print "zmiana"
    
    
    f = [vx,
         vy,                                     # dx/dt
         f_r*sinus*sign(kappa)
         - (mi*g*cos(alfa) + k1/m*vl + k2/m*vl**2)*cosinus
         ,
         g*sin(alfa) - f_r*cosinus*sign(kappa)
         - (mi*g*cos(alfa) + k1/m*vl + k2/m*vl**2)*sinus                                     # dx/dt
         ]    # dv/dt
    return f

def solver(t, x0, v0, alfa, mi, k1, k2, m, kappa=1/20.0, B=4):
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
        kappa: curvature - reciprocal of the radius (positive makes right turn)
        B : boundary value (in m/s) from with air drag becomes 
                proportional to the square of the velocity.
    '''

    '''
    Air drag is proportional to the square of velocity
    when the velocity is grater than some boundary value: B.
    k1 and k2 factors control whether we take square or linear proportion
    '''
    v0_length = mag(v0)
    if v0_length <= B:
        k2 = 0
    else:
        k1 = 0

    '''
    find cos and sin(beta) from velocity vector 
    where beta is the angle between x plane and velocity vector
    '''
    eps = 0.00001
    if(v0_length<=eps):
        cosinus=0.0
        sinus=1.0
    else:
        cosinus =  v0[0]/v0_length
        sinus = v0[1]/v0_length

    #Fdosr = m*v0_length**2*kappa
    #Fsciag = m*g*sin(alfa)*cosinus

    #print x0,"\t", v0, mag(v0)
    
    params = [alfa, mi, k1, k2, m, kappa, cosinus, sinus]

      
    w = odeint(_vectorfield, [x0[0], x0[1], v0[0], v0[1]], t, args=(params,) )
    #print w,"\t" #,t,"\t"
    
    wlist = w.tolist()
    y = [wlist[1][1],wlist[1][3]]
    x = [wlist[1][0],wlist[1][2]]

    return x,y