import visual
import numpy as np
from math import pi
import skier_with_air_resistance_force
import pylab

class Skier:
    '''
    Model of the skier
    '''
    def __init__(self, mi, alfa, k1, k2, m, x0, v0 ):
        '''
        Model of the skier. Arguments that models the races:
        Arguments:
            mi      - coefficient of friction. May vary for ex. on different waxes used.
            alfa    - slope degree. It is here - as a racer property, we can imagine 
                        unprofessional parrallel slalom with slightly different slope degree for recer
            k1      - factor for air friction force for small velocity
            k2      - factor for air friction force for higher velocity, dependent on
                        drag coefficient, density of the air, projected frontal area of the skier
            m       - mass
            x0      - initial position
            v0      - initial velocity
        '''
        self.mi, self.alfa, self.k1, self.k2, self.m = mi, alfa, k1, k2, m
        
        # values of position and velocity. Current values
        # are on the tail of the list
        self.positions = [x0]
        self.velocities = [v0]
        
        # time in second of the finish. None if not finished yet
        self.result = None
    
    def update_position(self, x):
        self.positions.append(x)
        
    def update_velocity(self, v):
        self.velocities.append(v)   
             
    def position(self):
        '''
        returns current position of the skier
        '''
        return self.positions[-1]

    def velocity(self):
        '''
        returns cuttent velocity of the skier
        '''
        return self.velocities[-1]        
    
class SkierSimulation:
    '''
    This class creates the world for the simulation.
    It takes care of representing time that passes and
    the movement of the skiers. 
    '''
    
    def __init__(self, solver, distance=700, interval=0.01, time_zoom=1, B=4):
        '''
        Arguments:
            solver    : solver for the simulation model
            distance  : distance in meters - length of the run
            interval  : time in seconds (may be float e.g. 0.1 ) telling about 
                          density with which we want to monitor the movement
                          (small interval means more continuous movement, big interval results
                          in "stepped motion")
            time_zoom : ratio between time passing rate in the simulation to 
                            time passing rate in the ordinary world. time_zoom > 1 results
                            in movement that is speeded up.
            B         : boundary value (in m/s) from with air drag becomes 
                            proportional to the square of the velocity.
        '''
        self.interval = interval
        self.distance = distance
        self.solver = solver
        self.current_time = 0.
        self.B = B
        # time_calibration specifies how fast time will be passing in the simulation
        self.time_calibration = int(time_zoom / interval)
        
        # list of all discret time values that were consider in the simulation
        self.timeline = [0]
        # racers is a list that holds registered racers.
        self.racers = []

    def __move_racer(self, racer):
        # if the racer finished the race, 
        # let him stay at the finishline
        if racer.result:
            racer.update_position(racer.position())
            racer.update_velocity(racer.velocity())
            return racer
        # if he hasn't reached the finishline, move him
        t0 = self.current_time
        t1 = t0 + self.interval
        result = self.solver([t0,t1], racer.position(), racer.velocity(), 
                             racer.alfa, racer.mi, racer.k1, racer.k2, racer.m, self.B)
        # result is a numpy ndarray, column with indez 0 is for t0,
        # we are interested in column with index 1 if for t1
        [x, v] = result.tolist()[1]
        racer.update_position(x)
        racer.update_velocity(v)
        # check if he's passing finishline now
        if x >= self.distance:
            racer.result = self.current_time
        return racer
                
    def run(self):
        '''
        Run the simulation with racers that had been previously added to the world
        by add_racer method.
        '''
        # create the scene with the plane at the top
        visual.scene.center = visual.vector(0,-25,0)
        visual.box(pos=(0,0,0), size=(12,0.2,12), color=visual.color.green)
        # create the visual objects that represent the racers (balls)
        balls = [ visual.sphere(pos=(index,0,0), radius=0.5) for index in xrange(len(self.racers))]
        
        while not reduce(lambda x, y: x and y, [racer.result for racer in self.racers]):
            # slow down the looping - allow only self.time_calibration
            # number of loop entries for a second
            visual.rate(self.time_calibration)
            # move the racers
            self.racers = [self.__move_racer(racer) for racer in self.racers]
            for ball, racer in zip(balls, self.racers):
                ball.pos.y = -racer.position()
            self.current_time += self.interval
            self.timeline.append(self.current_time)
            
    def add_racer(self, racer):
        '''
        Adds a racer to the simulation.
        Arguments:
            racer: an instance of Racer class
        '''
        self.racers.append(racer)
    

    

if __name__== '__main__':
    mi = 0.05 #waxed skis - typical value
    alfa= pi/12 #15` degrees
    roh = 1.32 #kg*(m^(-3))
    
    m = 60 #kg
    C = 0.6  #drag coficiant, typical values (0.4 - 1)

    A_A = 0.2 # m^2- medium position between upright and tucked
    k2_A = 0.5 * C * roh * A_A
    
    A_B = 0.16 # m^2- tucked position
    k2_B = 0.5 * C * roh * A_B
    
    k1 = 0.05 #imaginary value
    x0 = 0
    v0 = 0
    sim = SkierSimulation(solver=skier_with_air_resistance_force.solver, time_zoom=1)
    s_A = Skier(mi, alfa, k1, k2_A, m, x0, v0)
    s_B = Skier(mi, alfa, k1, k2_B, m, x0, v0)
    sim.add_racer(s_A)
    sim.add_racer(s_B)
    sim.run()
    print 'Time difference between A and B is %f seconds' %(s_A.result - s_B.result)
    pylab.plot(sim.timeline,s_A.positions, 
               sim.timeline,s_B.positions,)
    pylab.legend(('medium position', 'tucked position'), loc='lower right')
    pylab.xlabel("time in seconds")
    pylab.ylabel("distance in meters")
    pylab.grid(True)
    pylab.show()
