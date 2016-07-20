# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 9, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from hide.strategy import CoordSpec

def load_strategy(ctx):
    """
    Creates a dummy scanning strategy by always centering on RA/DEC 0/0
    
    :param ctx: The ctx instance with the paramterization
    
    :returns strategy: A dummy scanning strategy
    """
    
    start = ctx.strategy_start
    end   = ctx.strategy_end
    
    diff = int((end-start).total_seconds())
    step = ctx.params.strategy_step_size
    time = range(0, diff//step, step)
    return [CoordSpec(t, 0, 0, 0, 0) for t in time]