class Skier:
    '''
    Model of the skier
    '''
    def __init__(self, mi, alfa, k1, k2, m, x0, v0, kappa ):
        '''
        Model of the skier. Arguments that models the races:
        Arguments:
            mi      - coefficient of friction. May vary for ex. on different waxes used.
            alfa    - slope degree. It is here - as a racer property, we can imagine 
                        unprofessional parallel slalom with slightly different slope degree for racer
            k1      - factor for air friction force for small velocity
            k2      - factor for air friction force for higher velocity, dependent on
                        drag coefficient, density of the air, projected front area of the skier
            m       - mass
            x0      - initial position
            v0      - initial velocity
            kappa     - initial inverse of radius of the curve (1/r)
        '''
        self.mi, self.alfa, self.k1, self.k2, self.m, self.kappa = mi, alfa, k1, k2, m, kappa
        
        # values of position and velocity. Current values
        # are on the tail of the list
        self.positions = [x0]
        self.velocities = [v0]
        
        # functions that control the movement - that is
        # control changing of the radius
        self.radius_processors = []
        
        # time in second of the finish. None if not finished yet
        self.result = None
    
    def update_position(self, x):
        self.positions.append(x)
        
    def update_velocity(self, v):
        self.velocities.append(v)
        # steat the racer's turn based on velocity update, it stearin function if provided 

    def update_kappa(self):
        for processor in self.radius_processors:
            self.kappa = processor(self)  
             
    def position(self):
        '''
        returns current position of the skier
        '''
        return self.positions[-1]

    def velocity(self):
        '''
        returns current velocity of the skier
        '''
        return self.velocities[-1]        
    