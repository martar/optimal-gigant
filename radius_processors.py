''''
This module define processord that can control the change of radius 
each processor function shoud take a Skier as an argument and
return the apprioprate ksi, that the racer should take,
to perform some actin defined by the filter.
'''
from visual import mag

def falling_leaf(racer):
    '''
    This processor attempts to stear the motion of falling leaf..
    so the racer makes a cut curve, and when he looses velocity, 
    we starts to move backwards.
    '''
    try:
        last = racer.velocities[-1][1]
        before_last = racer.velocities[-2][1]
        # if the velocity in y axis was going upwards and than went downwords
        if before_last < 0 and last > 0:
            return -racer.ksi
    except:
        # racer just started to be moving, so he doesn't have at least 
        # 2 entries in the list of history velocities
        pass
    return racer.ksi

def cutting_turns(racer):
    '''
    This processor attempts to stear the motion of cut turns
    '''   
    try:
        last = mag(racer.velocities[-1])
        before_last = mag(racer.velocities[-2])
        before_before_last = mag(racer.velocities[-3])
        
        if (before_last - before_before_last) >0 and (last - before_last) < 0:
            return -racer.ksi
    except:
        # racer just started to be moving, so he doesn't have at least 
        # 3 entries in the list of history velocities
        pass
    return racer.ksi

def tightening_turns(racer):
    '''
    This processor attempts to stear the motion of tighter and thiter turns
    '''
    try:
        last = mag(racer.velocities[-1])
        before_last = mag(racer.velocities[-2])
        before_before_last = mag(racer.velocities[-3])
        
        if (before_last - before_before_last) >0 and (last-before_last) < 0:
            return -racer.ksi + 0.05 *racer.ksi
    except:
        # racer just started to be moving, so he doesn't have at least 
        # 3 entries in the list of history velocities
        pass
    return racer.ksi

