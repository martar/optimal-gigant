from controller import Controller

class RightTurnController(Controller):
    def __init__(self, kappa):
        self.kappa = kappa
        
    def desired_curvature(self, position, kappa, sign_omega, *args, **kwargs):
        # we want to always use kappa value declared at the init, 
        # we don't care about most recent kappa, we just change the 
        # direction
        return self.kappa, -1

class LeftTurnController(Controller):
    def __init__(self, kappa):
        self.kappa = kappa
        
    def desired_curvature(self, position, kappa, sign_omega, *args, **kwargs):
        # we want to always use kappa value declared at the init, 
        # we don't care about most recent kappa, we just change the 
        # direction
        return self.kappa, 1

class StraightGoingController(Controller):
    
    def desired_curvature(self, position, kappa, sign_omega, *args, **kwargs):
        return 0, 0

class HopTurningController:
    '''
    Sample controller which decides when to change the subcontroller 
    to the one which has totally different curvature (kappa,0 or -kappa)
    
    The boundaries of changes are evaluated from the boundary_val which
    indicates fraction of the radius. When starting x coordinate is 0
    then X coordinate varies from 0 to 2*1/kappa, so the boundaries are:
    1/kappa - boundary_val/kappa and 1/kappa + boundary_val/kappa 
    
    FIXME kappa can't be equal to zero
    '''
    def __init__(self, slalom, right_turning_controller, left_turning_controller, straight_controller, kappa, boundary_val = 0.2):
        self.slalom = slalom
        self.right_turning_controller = right_turning_controller
        self.left_turning_controller = left_turning_controller
        self.straight_controller = straight_controller
        
        #values for evaluating the boundaries of changes
        self.boundary = boundary_val/kappa
        self.planned_r = 1/kappa
        
        # positions of previous and next gate
        self.prev_gate = None
        self.next_gate = None
    
    def control(self, position, kappa, start_x, sin_beta,cos_beta,sign_omega, *args, **kwargs):
        x,_,_ = position
        cur_x = x

        #find the boundaries of the changes - left and right        
        lbound = start_x + self.planned_r - self.boundary
        rbound = start_x + self.planned_r + self.boundary
  
        #choose the controller basing on the current position
        if abs(cur_x) < lbound:
            return self.right_turning_controller.control(position, kappa, sign_omega, *args, **kwargs)
        elif abs(cur_x) > rbound:
            return self.left_turning_controller.control(position, kappa, sign_omega, *args, **kwargs)
        else:
            return self.straight_controller.control(position, kappa, sign_omega, *args, **kwargs)
