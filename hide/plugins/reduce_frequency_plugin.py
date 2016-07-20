# Copyright (C) 2013 ETH Zurich, Institute for Astronomy

'''
Created on Mar 18, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

class Plugin(object):
    '''
    Combines the time ordered data for all frequencies
    '''

    def __init__(self, ctx):
        '''
        Constructor
        '''
        self.ctx = ctx
    
    def reduce(self, ctxList):
        tod_vx = []
        tod_vy = []
        for ctx in ctxList:
            tod_vx.append(ctx.signals)
        
        #TODO: no data for Y-Polarization
        tod_vx = np.array(tod_vx)
        tod_vy = np.array(tod_vy)
        self.ctx.tod_vx = tod_vx
        self.ctx.tod_vy = tod_vy