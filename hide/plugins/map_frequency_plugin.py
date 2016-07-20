# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 11, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals


class Plugin(object):
    '''
    Maps the frequencies to the plugin collection.
    '''
    
    def __init__(self, ctx):
        '''
        Constructor
        '''
        self.ctx = ctx
    
    def getWorkload(self):
        
        for idx, frequency in enumerate(self.ctx.frequencies):
#             gc.collect()
            ctx = self.ctx.copy()
            ctx.frequency = frequency
            ctx.frequency_idx = idx
            ctx.beam_profile = self.ctx.beam_profiles[idx]
            ctx.beam_norm = self.ctx.beam_norms[idx]
            del ctx.beam_profiles
            del ctx.beam_norms
            yield ctx