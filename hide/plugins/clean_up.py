# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Sep 14, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from ivy.plugin.base_plugin import BasePlugin

class Plugin(BasePlugin):
    """
    Cleans up the context to avoid a memory leak
    """

    def __call__(self):
        del self.ctx.tod_vx
        del self.ctx.tod_vy
        del self.ctx.frequencies
        del self.ctx.strategy_coords
        del self.ctx.beams
        del self.ctx.tod_vx_rfi 
        
    def __str__(self):
        return "Clean up"
    
