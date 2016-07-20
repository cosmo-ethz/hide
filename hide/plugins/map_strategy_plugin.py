# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 11, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from datetime import timedelta

class Plugin(object):
    '''
    Maps the strategy coordinates to the plugin collection.
    '''
    
    def __init__(self, ctx):
        self.ctx = ctx
    
    def getWorkload(self):
        
        block_size = int(self.ctx.params.time_range / self.ctx.params.strategy_step_size)
        verbose = self.ctx.params.verbose
        
        for idx in range((len(self.ctx.strategy)-1)//block_size+1):
            ctx = self.ctx.copy()
            ctx.strategy = None
            coords = self.ctx.strategy[idx*block_size : min(((idx+1)*block_size), len(self.ctx.strategy))]
            ctx.strategy_coords = coords
            ctx.strategy_idx = idx
            ctx.batch_start_date = self.ctx.strategy_start + timedelta(seconds=coords[0].time)
            
            if verbose:
                print("Processing", ctx.batch_start_date)
            yield ctx