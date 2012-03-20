from visual import *
from math import *


g = 9.80665

class GravityMovement:
    '''
    Abstracion of an object that can move on an inclined plane.
        mi - coefficient of friction
        alfa - slope degree (degree between  B and C)
       |\     
       |  \
    A  |    \  C
       | alfa \
       |________\
           B   
        init_position - initial posiiton of the moving object (sphere) on the scene
        init_velocity - initial velosity
    '''
    def __init__(self, mi=0.2, alfa=math.pi/6.0, init_pos=(0,0,0), init_v = (0,0,0)):
        self.mi = mi
        self.alfa = alfa
        self.ball = sphere(pos=init_pos, radius=0.5, color=color.cyan)
        self.ball.init_pos = init_pos
        self.ball.trail = curve(color=color.cyan)
        
    def move(self, t):
        '''
        Moves the object in rules of uniformly accelerated motion. Velocity is hard coded now.
        No resistance force, only fricion.
        '''
        a = -g*(sin(self.alfa)-self.mi*cos(self.alfa))
        newPos = vector(a*cos(self.alfa), a*sin(self.alfa), 0)*t*t/2.0
        if t!=0:
            print a/t
        self.ball.pos =  vector(self.ball.init_pos) + newPos
        self.ball.trail.append(pos=self.ball.pos)
        
    def reset_position(self):
        '''
        Resets object position to initial value and resets its trail.
        '''
        self.ball.pos = self.ball.init_pos
        self.ball.trail.visible = False
        self.ball.trail = curve(color=color.cyan)
    
def create_scene():
    '''
    creates scene for animation.
    '''
    wallD = box(pos=(0,-6,0), size=(12,0.2,12), color=color.green)
    wallU = box(pos=(0,6,0), size=(12,0.2,12), color=color.green)
    ball1 = GravityMovement(init_pos=(0,6,0), alfa=math.pi/3.0, mi=0.2)
    ball2 = GravityMovement(init_pos=(1,6,0), alfa=math.pi/6.0, mi=0.2)
    ball3 = GravityMovement(init_pos=(2,6,0), alfa=math.pi/3.0, mi=0.4)
    deltat = 0.005
    t = 0
    move = True
    balls = [ball1, ball2, ball3]
    while True:
        rate(400)
        if scene.kb.keys: # is there an event waiting to be processed?
            s = scene.kb.getkey() # obtain keyboard information
            if s == 'r':
                # reset the scene
                [ball.reset_position() for ball in balls]
                t = 0
                move = True
        if move:
            for ball in balls:
                ball.move(t)
                if ball.ball.pos.y < wallD.pos.y:
                    move = False
            t = t + deltat
        
if __name__ == '__main__':
    create_scene()