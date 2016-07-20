# Copyright (C) 2013 ETH Zurich, Institute for Astronomy

'''
Created on Mar 18, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

class Plugin(object):
    '''
    Combines all signals to time ordered data
    '''


    def __init__(self, ctx):
        '''
        Constructor
        '''
        self.ctx = ctx
    
    def reduce(self, ctxList):
        tod_vx = []
        for ctx in ctxList:
            tod_vx.append(ctx.signal)
        
        tod_vx = np.array(tod_vx)
        self.ctx.tod_vx = tod_vx