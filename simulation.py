from visual import *
from math import *

ball = sphere(pos=(0,6,0), radius=0.5, color=color.cyan)
ball3 = sphere(pos=(1,6,0), radius=0.5, color=color.red)

ball2 = sphere(pos=(2,6,0), radius=0.5, color=color.blue)

wallU = box(pos=(0,-6,0), size=(12,0.2,12), color=color.green)
wallD = box(pos=(0,6,0), size=(12,0.2,12), color=color.green)


g = 9.81
mi = 0.2


alfa = math.pi/6.0 # 30 degrees
alfa2 = math.pi/3.0 # 60 degrees

deltat = 0.005
t = 0
vscale = 0.1

ball.trail = curve(color=ball.color)

while True:
    rate(100)
    ball.velocity = vector(3, -g*(sin(alfa)-mi*cos(alfa)), 0)*t
    ball3.velocity = vector(3, -g*(sin(alfa)-mi*2*cos(alfa)), 0)*t
    
    ball2.velocity = vector(3, -g*(sin(alfa2)-mi*cos(alfa2)), 0)*t
    ball.pos = ball.pos + ball.velocity*deltat
    ball2.pos = ball2.pos + ball2.velocity*deltat
    ball3.pos = ball3.pos + ball3.velocity*deltat        
    ball.trail.append(pos=ball.pos)
    t = t + deltat