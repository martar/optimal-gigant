'''
    This module defines the structure of controllers that decide what the next
    kappa should be.
    There can be a hierarchy of controllers: for example a master controller that
    decides which lower level controller should be used in a given moment of time.
    For example a master controller decides that in a given moment a racer should 
    change his direction, so he changes the racer's controller to 'changing direction' controller
    and then when he decides that changing direction ended, he reintroduces 'regular' controller to handle racer movement
'''

class Controller:
    '''
    Skeleton for controllers.
    components that uses the controller should be interested only in control method.
    Implementation of the controller should mainly focus on all: desired_curvature, possible_curvature,
    and also probably 'control'
    '''    
    def desired_curvature(self, racer, *args, **kwargs):
        '''
        returns a curvature that is decided to be the best in terms
        of skier performance on his route
        '''
        # TODO this is a method stub
        return racer.kappa
    
    def possible_curvature(self, desired_curvature, racer, *args, **kwargs):
        '''
        returns a curvature that is computed based on the result
        of desired_curvature and confronting this to physics
        conditions and limitations that they causes.
        '''

        # TODO this is a method stub
        # TODO logic should go here
        return desired_curvature
    
    def control(self, racer, *args, **kwargs):
        '''
        this is a method that returns the next curvature
        that the racer should take in respect to provided conditions
        '''
        desired_curvature = self.desired_curvature(racer, *args, **kwargs)
        possible_curvature = self.possible_curvature(desired_curvature, racer, *args, **kwargs)
        return possible_curvature

