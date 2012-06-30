from visual import mag
import visual
class Skier:
    '''
    Model of the skier
    '''
    def __init__(self, mi, alfa, k1, k2, B, m, x0, v0, kappa, slalom, solver, kappa_controller, color="blue",  sign_omega=-1):
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
            slalom - list of tuples with slalom gate's positions
            solver - solver of phicics move equation
            kappa_controller - controller of kappa changes - stearing
            sign_omega - signum of first derivative of fi ( angular velocity) - its value is a direction 
                of the movement. It's value is 
                    1, when skier turns left
                    0, when skier go straigth
                    -1, when skier turns right
            color - string describing the color of the racei in the simulation (just for the convinience) basic collors like
                blue, red, yellow etc are supported
        '''
        self.mi, self.alfa, self.k1, self.k2, self.B, self.m= mi, alfa, k1, k2, B,  m
        self.slalom = slalom
        self.solver, self.kappa_controller = solver, kappa_controller
        # values of position and velocity. Current values
        # are on the tail of the list
        self.positions = [x0]
        self.velocities = [v0]
        self.kappas = [kappa]
        self.sign_omegas = [sign_omega]
        self.color = color
        # time in second of the finish. None if not finished yet
        self.result = None
    
    def __compute_sin_cos_beta(self):
        '''
        find cos_beta and sin_beta from velocity vector 
        where beta is the angle between x plane and velocity vector
        '''
        v0_length = mag(self.velocities[-1])
        eps = 0.00001
        
        if(v0_length<=eps):
            cos_beta=0.0
            sin_beta=1.0
        else:
            cos_beta =  self.velocities[-1][0]/v0_length
            sin_beta = self.velocities[-1][1]/v0_length
        return sin_beta, cos_beta
    
    def __compute_next_position_and_velocity(self, t0, t1, sin_beta, cos_beta):
        '''
        compute the next position and velocity of the racer, based on 
        actual racer phisical conditions. returns two tuples 
        (xx,vx), (xy,vy)
        ''' 
        result_x, result_y = self.solver([t0,t1], self.positions[-1], self.velocities[-1],
                                 sin_beta, cos_beta,
                                 self.alfa, self.mi, self.k1, self.k2, self.m, 
                                 B=self.B, kappa=self.kappas[-1], sign_omega=self.sign_omegas[-1])
        return result_x, result_y       
     
    def move(self, t0, t1):
        '''
        move the racer between t0 and t1 time quant
        '''
        sin_beta, cos_beta = self.__compute_sin_cos_beta()
        (xx, vx), (xy, vy) = self.__compute_next_position_and_velocity(t0,t1, sin_beta, cos_beta)
        self.positions.append(visual.vector(xx,xy))
        self.velocities.append(visual.vector(vx,vy))
        new_kappa, new_sign_omega = self.kappa_controller.control(position=self.positions[-1], kappa=self.kappas[-1],
                                                  sign_omega=self.sign_omegas[-1],
                                                  start_x=self.positions[0][0], cos_beta=cos_beta, sin_beta=sin_beta)
        self.kappas.append(new_kappa)
        self.sign_omegas.append(new_sign_omega)
        
    def stay_still(self):
        '''
        stay in the same place, between time quant
        '''
        self.positions.append((self.positions[-1]))
        self.velocities.append((self.velocities[-1]))
        self.kappas.append(self.kappas[1])
        self.sign_omegas.append(self.sign_omegas[-1])
        
    def __next_gate(self):
        '''
        returns the possition of next gate
        '''
        pass

              
    