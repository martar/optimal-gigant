# -*- coding: utf-8 -*-

from math import sin, cos, sqrt
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
    
    f_R = vl**2*abs(kappa)
    # it's not the valu of the force -> no mass in eq
    f_r = f_R + sign(kappa)*g*sin(alfa)*cosinus
    
    '''
    if f_r < 0:
        f_r = sign(kappa)*g*sin(alfa)*cosinus
        f_R = 0
    '''
     
    '''todo wiki
    na sile nacisku wplywa tez sila od�rodkowa, jak jad� po kole to tarcie si� zwi�ksza, 
    i wida� �e jak jad� na wprost to mog� dalej pojecha�
    '''
    N = sqrt ( (g*cos(alfa))**2 + (f_R)**2 )
    
    f = [vx,
         vy,                                     # dx/dt
         f_r*sinus*sign(kappa)
         - (mi*N + k1/m*vl + k2/m*vl**2)*cosinus
         ,
         g*sin(alfa) - f_r*cosinus*sign(kappa)
         - (mi*N + k1/m*vl + k2/m*vl**2)*sinus                                     # dx/dt
         ]    # dv/dt
    return f

def solver(t, x0, v0, sin_beta, cos_beta, alfa, mi, k1, k2, m, kappa=1/20.0, B=4):
    '''
    Solves the move equation. Move happens on an inclined plane with 
    rules of uniformly accelerated motion.
    Air resistance force is dependent with velocity, friction is constant.
    Arguments:
        x0: initial position - vector
        v0: initial velocity in m/s - vector
        cos_beta,sin_beta - beta is the angle between x plane and velocity vector
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
    
    params = [alfa, mi, k1, k2, m, kappa, cos_beta, sin_beta]
      
    w = odeint(_vectorfield, [x0[0], x0[1], v0[0], v0[1]], t, args=(params,) )
    
    #print w,"\t" #,t,"\t"
    
    wlist = w.tolist()
    y = [wlist[1][1],wlist[1][3]]
    x = [wlist[1][0],wlist[1][2]]

    return x,y