from controller import Controller

class SampleCurvatureController(Controller):
    pass

class SampleChangeController(Controller):
    
    def desired_curvature(self, racer, *args, **kwargs):
        return -racer.kappa


class DirectionDecisionController:
    '''
    Sample master controller that decides when other controllers should be used    
    '''
    def __init__(self,  movement_controller, change_controller, x_change=10):
        self.movement_controller = movement_controller
        self.change_controller = change_controller
        # what is the x when we should change direction
        self.x_change= x_change
        self.recently_passed_change = False
    
    def control(self, racer, *args, **kwargs):
        x,y = racer.position()[0], racer.position()[1]
        if x > self.x_change-0.1 and x <  self.x_change+0.1:
            if not self.recently_passed_change:
                self.recently_passed_change = True
                # change controller should least only for one quantum of time - change the sign
                return self.change_controller.control(racer, *args, **kwargs)
        else:
            self.recently_passed_change = False
        return self.movement_controller.control(racer, *args, **kwargs)
    
if __name__ == '__main__':
    from skier import Skier
    from visual import vector
    from math import pi
    import skier_with_air_resistance_force
    from simulation import SkierSimulation
    from hop_turn_controller import HopTurningController,StraightGoingController,RightTurnController,LeftTurnController
    mi = 0.05 #waxed skis - typical value
    
    alfa = pi/6
    roh = 1.32 #kg*(m^(-3))
    
    m = 60 #kg
    C = 0.6  #drag coefficient, typical values (0.4 - 1)
    
    A= 0.2 # m^2- medium position between upright and tucked

    k2 = 0.5 * C * roh * A

    kappa = 1/20.0
    k1 = 0.05 #imaginary value
    x0 = vector(0,0)
    v0 = vector(0,19)   #'''sqrt(2000)'''
    racer = Skier(mi, alfa, k1, k2, m, x0, v0, kappa)
    racer2 = Skier(mi, alfa, k1, k2, m, x0, v0, kappa)
    racer.controller = DirectionDecisionController(movement_controller=SampleCurvatureController(),
                                                  change_controller=SampleChangeController())
    racer2.controller = HopTurningController(right_turning_controller=RightTurnController(kappa),
                                    left_turning_controller=LeftTurnController(kappa),
                                    straight_controller=StraightGoingController(), 
                                    kappa=kappa, boundary_val=0.2)
    sim = SkierSimulation(distance=200, interval=0.001, solver=skier_with_air_resistance_force.solver, time_zoom=100)
    sim.add_racer(racer)
    sim.add_racer(racer2)
    sim.run()
    