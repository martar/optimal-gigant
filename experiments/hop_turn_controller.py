from controller import Controller

class RightTurnController(Controller):
    def __init__(self, kappa):
        self.kappa = kappa
        
    def desired_curvature(self, racer, *args, **kwargs):
        return self.kappa

class LeftTurnController(Controller):
    def __init__(self, kappa):
        self.kappa = kappa
        
    def desired_curvature(self, racer, *args, **kwargs):
        return -self.kappa

class StraightGoingController(Controller):
    
    def desired_curvature(self, racer, *args, **kwargs):
        return 0

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
    def __init__(self, right_turning_controller, left_turning_controller, straight_controller, kappa, boundary_val = 0.2):
        self.right_turning_controller = right_turning_controller
        self.left_turning_controller = left_turning_controller
        self.straight_controller = straight_controller
        
        #values for evaluating the boundaries of changes
        self.boundary = boundary_val/kappa
        self.planned_r = 1/kappa
    
    def control(self, racer, *args, **kwargs):
        start_x = racer.positions[0][0]
        cur_x = racer.position()[0]

        #find the boundaries of the changes - left and right        
        lbound = start_x + self.planned_r - self.boundary
        rbound = start_x + self.planned_r + self.boundary
        
        #choose the controller basing on the current position
        if cur_x < lbound:
            return self.right_turning_controller.control(racer, *args, **kwargs)
        elif cur_x > rbound:
            return self.left_turning_controller.control(racer, *args, **kwargs)
        else:
            return self.straight_controller.control(racer, *args, **kwargs)
