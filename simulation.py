import visual
from visual import mag

class SkierSimulation:
    '''
    This class creates the world for the simulation.
    It takes care of representing time that passes and
    the movement of the skiers. 
    '''
    
    def __init__(self, solver, distance=40, interval=0.01, time_zoom=1, B=4):
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
            racer.update_kappa()
            return racer
        # if he hasn't reached the finishline, move him
        t0 = self.current_time
        t1 = t0 + self.interval
        
        '''
        find cos_beta and sin_beta from velocity vector 
        where beta is the angle between x plane and velocity vector
        '''
        v0_length = mag(racer.velocity())
        eps = 0.00001
        
        if(v0_length<=eps):
            cos_beta=0.0
            sin_beta=1.0
        else:
            cos_beta =  racer.velocity()[0]/v0_length
            sin_beta = racer.velocity()[1]/v0_length
            
        result_x, result_y = self.solver([t0,t1], racer.position(), racer.velocity(), 
                                 sin_beta, cos_beta,
                                 racer.alfa, racer.mi, racer.k1, racer.k2, racer.m, 
                                 B=self.B, kappa=racer.kappa)
        #FIXME
        # result is a numpy ndarray, column with index 0 is for t0,
        # we are interested in column with index 1 if for t1
        [xx, vx] = result_x
        [xy, vy] = result_y
        
        racer.update_position(visual.vector(xx,xy))
        racer.update_velocity(visual.vector(vx,vy))
        #FIXME steering
        racer.update_kappa()
        
        # check if he's passing finishline now
        if xy >= self.distance:
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
        for ball in balls:
            ball.trail  = visual.curve(color=visual.color.blue)
        while not reduce(lambda x, y: x and y, [racer.result for racer in self.racers]):
            # slow down the looping - allow only self.time_calibration
            # number of loop entries for a second
            visual.rate(self.time_calibration)
            # move the racers
            self.racers = [self.__move_racer(racer) for racer in self.racers]
            for ball, racer in zip(balls, self.racers):
                ball.pos.y = -racer.position()[1]
                ball.pos.x = racer.position()[0]
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
