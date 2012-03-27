from visual import *
import skier_with_air_resistance_force
import numpy as np

class SkierSimulation():
    '''
    Arguments:
        start_time: time in seconds (from the beggining of the movement)
                    when the simulation starts
        end_time: time in seconds when the simulation ends 
                (from the begging of the movement)
        interval: interval with which we wand to monitor movement

        time_zoom : how many times faster does one second passes in our 
                    simulated world than in regular world
        
    '''
    def __init__(self, start_time=0, end_time=5, interval=0.01, time_zoom=1):
        self.start_time = start_time
        self.end_time = end_time
        self.interval = interval
        self.time_zoom = time_zoom
        # number of steps that we will consider
        self.steps = (end_time - start_time) / interval
        self.timeline = np.linspace(start_time, end_time, self.steps)
        # time_calibration specifies how fast time will be passing in the simulation
        self.time_calibration = int(time_zoom / interval)
        
        # racer is a abstraction od the skier
        self.racers = []
        
    def run(self):
        scene.center = vector(0,-25,0)
        box(pos=(0,0,0), size=(12,0.2,12), color=color.green)
        balls = []
        i=0
        for racer in self.racers:
            balls.append(sphere(pos=(0,0,0), radius=0.5, color=color.cyan))
        i=0
        for moment in self.timeline:
            rate(self.time_calibration)
            for ball, xvector in zip(balls, self.racers):
                ball.pos.y = -xvector[i]
            print round(moment,2)
            i+=1
            
    def add_racer(self, mi, alfa, k, solver, w=[0,0]):
        '''
        Adds a racer to the simulation
        Arguments:
        w: vector of initial conditions (for time = 0) w = [x, v]
            x: initial position (one dimension vector???)
            v: initila velocity in m/s
        alfa: slope degree (degree between  B and C)
               |\     
               |  \
            A  |    \  C
               | alfa \
               |________\
                   B   
        mi: coefficient of friction       
        k: resistance factor (with mass "inside")
        solver: function that solves move equasion for this racer
        '''
        movement = solver( self.timeline, [alfa,mi,k], w)[:,0]
        self.racers.append(movement)

if __name__== '__main__':
    sim = SkierSimulation()
    sim.add_racer(0.2, math.pi/3, 0.1, skier_with_air_resistance_force.solver, w=[0,5])
    sim.add_racer(0.2, math.pi/3, 0.01, skier_with_air_resistance_force.solver)
    sim.run()
