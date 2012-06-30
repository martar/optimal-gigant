import visual
from visual import mag
import random

class SkierSimulation:
    '''
    This class creates the world for the simulation.
    It takes care of representing time that passes and
    the movement of the skiers. 
    '''
    
    def __init__(self, distance=40, interval=0.01, time_zoom=1, B=4):
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
        self.current_time = 0.
        self.B = B
        # time_calibration specifies how fast time will be passing in the simulation
        self.time_calibration = int(time_zoom / interval)
        
        # list of all discret time values that were consider in the simulation
        self.timeline = [0]
        # racers is a list that holds registered racers.
        self.racers = []

    
        #FIXME
        # result is a numpy ndarray, column with index 0 is for t0,
        # we are interested in column with index 1 if for t1

        
    def __move_racer(self, racer):
        # if the racer finished the race, 
        # let him stay at the finishline
        if racer.result:
            racer.stay_still()
            return racer
        # if he hasn't reached the finishline, move him
        t0 = self.current_time
        t1 = t0 + self.interval
    
        racer.move(t0, t1)
        
        # check if he's passing finishline now
        if racer.positions[-1][1] >= self.distance:
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
        for ball, racer in zip(balls, self.racers):
            color = visual.color.blue
            try:
                # try to set the color given by a string
                color = getattr(visual.color, racer.color)
            except AttributeError:
                pass
            ball.trail  = visual.curve(color=color)
        while not reduce(lambda x, y: x and y, [racer.result for racer in self.racers]):
            # slow down the looping - allow only self.time_calibration
            # number of loop entries for a second
            visual.rate(self.time_calibration)
            # move the racers
            for racer in self.racers:
                self.__move_racer(racer) 
                
            for ball, racer in zip(balls, self.racers):
                ball.pos.y = -racer.positions[-1][1]
                ball.pos.x = racer.positions[-1][0]
                ball.trail.append(pos=ball.pos)
                
            self.current_time += self.interval
            self.timeline.append(self.current_time)
            
    def add_racer(self, racer):
        '''
        Adds a racer to the simulation.
        Arguments:
            racer: an instance of Racer class
        '''
        self.racers.append(racer)
