from controller import Controller

class TurnController(Controller):
    '''
    Our desired kappa is the one which enables us to properly pass a next gate.
    
    If racer hasn't started the turn, we compute kappa accordingly to the position of both
    skier and next gate. Then we check if it is proper. If it is, racer can start the turn, 
    otherwise he goes straight (kappa = 0).
    
    If skier is turning we just return the same kappa.
    '''
    def desired_curvature(self, racer, *args, **kwargs):

        #if we are not turning yet, find the kappa value
        if racer.kappa == 0:
            next_gate = kwargs['next_gate']
            
            x_gate = next_gate[0]
            y_gate = next_gate[1]
            
            racer_x = racer.position()[0]
            racer_y = racer.position()[1]

            #if we are below the gate we missed it
            if y_gate < racer_y:
                #FIXME upss! there is a problem!
                pass
                
            del_x = abs(x_gate - racer_x)
            del_y = y_gate - racer_y
            
            #FIXME find out the values of sinus and cosinus
            #eg. it can be computed from racer.velocity()
            desired_R = del_y/abs(cosinus)
            
            #if we can pass the gate with desired_R
            if desired_R > del_x + desired_R*abs(sinus):
                if kwargs['turn'] == 'right':
                    return 1/desired_R
                elif kwargs['turn'] == 'left':
                    return -1/desired_R
            #we can't turn yet
            return 0
        
        #we are already turning, just return the same kappa 
        else:
            return racer.kappa

class StraightGoingController(Controller):
    
    def desired_curvature(self, racer, *args, **kwargs):
        return 0

class HopTurningController:
    '''
    Sample controller which decides when to change the subcontroller 
    to the one which has totally different curvature (kappa,0 or -kappa).
    Kappa is computed basing on the current position and the position 
    of the next gate.
    
    The boundaries of changes are evaluated from the boundary_val which
    indicates fraction of the half of the distance between the nearest gates. 
     
    Inside boundaries kappa is 0, outside we try to make a proper turn.
    If we are before the first gate we try to make a turn at once. 
    '''
    def __init__(self, turning_controller, straight_controller, boundary_val = 0.2):
        self.turning_controller = turning_controller
        self.straight_controller = straight_controller
        
        #values for evaluating the boundaries of changes
        self.boundary = boundary_val
    
    def control(self, racer, *args, **kwargs):
        start_x = racer.positions[0][0]
        cur_x = racer.position()[0]

        kwargs['next_gate'] = next_gate

        #we are before the first gate
        if not prev_gate:
            #first gate is on the left -> try right turn
            if next_gate[0] < start_x:
                kwargs['turn'] = 'right'
            #first gate is on the right -> try left turn
            else:
                kwargs['turn'] = 'left'
            return self.turning_controller(racer, *args, **kwargs)
        #if we have both gates prev and next gate
        else:
            middle = (next_gate[0] + prev_gate[0])/2
            
            #find the boundaries of the changes - left and right
            #find the gate further to the left
            x_min = min(next_gate[0],prev_gate[0])        
            lbound = x_min + middle - self.boundary*(middle-x_min)
            rbound = x_min + middle + self.boundary*(middle-x_min)
            
            #choose the controller basing on the current position
            if cur_x < lbound:
                kwargs['turn'] = 'right'
                return self.turning_controller.control(racer, *args, **kwargs)
            elif cur_x > rbound:
                kwargs['turn'] = 'left'
                return self.turning_controller.control(racer, *args, **kwargs)
            else:
                return self.straight_controller.control(racer, *args, **kwargs)
