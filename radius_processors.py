''''
This module define processors that can control the change of radius 
each processor function should take a Skier as an argument and
return the appropriate kappa, that the racer should take,
to perform some action defined by the filter.
'''
from visual import mag

def falling_leaf(racer):
    '''
    This processor attempts to steer the motion of falling leaf..
    so the racer makes a cut curve, and when he looses velocity, 
    we starts to move backwards.
    '''
    try:
        last = racer.velocities[-1][1]
        before_last = racer.velocities[-2][1]
        # if the velocity in y axis was going upwards and than went downwords
        if before_last < 0 and last > 0:
            return -racer.kappa
    except:
        # racer just started to be moving, so he doesn't have at least 
        # 2 entries in the list of history velocities
        pass
    return racer.kappa

def cutting_turns(racer):
    '''
    This processor attempts to stear the motion of cut turns
    '''   
    try:
        last = mag(racer.velocities[-1])
        before_last = mag(racer.velocities[-2])
        before_before_last = mag(racer.velocities[-3])
        
        if (before_last - before_before_last) >0 and (last - before_last) < 0:
            return -racer.kappa
    except:
        # racer just started to be moving, so he doesn't have at least 
        # 3 entries in the list of history velocities
        pass
    return racer.kappa

def tightening_turns(racer):
    '''
    This processor attempts to steer the motion of tighter and tighter turns
    '''
    try:
        last = mag(racer.velocities[-1])
        before_last = mag(racer.velocities[-2])
        before_before_last = mag(racer.velocities[-3])
        
        if (before_last - before_before_last) >0 and (last-before_last) < 0:
            return -racer.kappa + 0.05 *racer.kappa
    except:
        # racer just started to be moving, so he doesn't have at least 
        # 3 entries in the list of history velocities
        pass
    return racer.kappa

def circle(racer):
    '''
    This processor does not change the kappa
    If the skier has sufficient speed it will make a circle
    '''
    return racer.kappa