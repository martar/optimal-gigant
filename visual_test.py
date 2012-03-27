from visual import *
import skier_with_air_resistance_force
import numpy as np

class SkierSimulation:
    '''
    This class creates the world for the simulation.
    It takes care of representing time that passes and
    the movement of the skiers. 
    '''
    
    def __init__(self, end_time=5, interval=0.01, time_zoom=1):
        '''
        Arguments:
            end_time: time in seconds when the simulation ends. For the
                        begginging of the simulation we set time=0 in our world
            interval: time in seconds (may be float for ex. 0.1 ) telling about 
                      density with which we want to monitor the movement
                      (small interval means more continous movement, big interval results
                      in "stepped motion")
            time_zoom : ratio between time passing rate in the simulation to 
                        time passing rate in the ordinary world. time_zoom > 1 results
                        in movement that is speeded up.
        '''
        # number of steps that we  consider
        steps = end_time / interval
        # list with all discrate time moments considered in the simulation
        self.timeline = np.linspace(0, end_time, steps)
        # time_calibration specifies how fast time will be passing in the simulation
        self.time_calibration = int(time_zoom / interval)
        
        # racer_tracs is a list that holds trac for every ragistered racer.
        # The trac is a list of positions of the racer in all discrate moments 
        # of time considered in this simulation (in self.timeline)
        self.racer_tracs = []
        
    def run(self):
        '''
        Run the simulation with racers that had been previously added to the world
        by add_racer method.
        '''
        # create the scene with the plane at the top
        scene.center = vector(0,-25,0)
        box(pos=(0,0,0), size=(12,0.2,12), color=color.green)
        
        # create the visual objects that represent the racers (balls)
        balls = [ sphere(pos=(index,0,0), radius=0.5) for index in xrange(len(self.racer_tracs))]
        
        for moment in xrange(len(self.timeline)):
            # slow down the looping - allow only self.time_calibration
            # number of loop enrties for a second
            rate(self.time_calibration)
            
            for ball, racer_trac in zip(balls, self.racer_tracs):
                ball.pos.y = -racer_trac[moment]
            
    def add_racer(self, mi, alfa, k, solver, w=[0,0]):
        '''
        Adds a racer to the simulation.
        Arguments:
        w: vector of initial conditions (for time = 0) w = [x, v]
            x: initial position (one dimension)
            v: initila velocity in m/s (one dimension)
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
        self.racer_tracs.append(movement)

if __name__== '__main__':
    sim = SkierSimulation()
    sim.add_racer(0.2, math.pi/3, 0.1, skier_with_air_resistance_force.solver, w=[0,5])
    sim.add_racer(0.2, math.pi/3, 0.01, skier_with_air_resistance_force.solver)
    sim.run()
