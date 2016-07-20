# Copyright (C) 2016 ETH Zurich, Institute for Astronomy

'''
Created on Mar 23, 2016

author: seehars
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from ivy.plugin.base_plugin import BasePlugin

import importlib
import numpy as np

class Plugin(BasePlugin):
    """
    Adds a time-constant, elevation dependent background to the TOD.
    """

    def __call__(self):
        #load module
        mod = importlib.import_module(self.ctx.params.instrument)
        
        #delegate loading of background as a function of elevation
        bg_model = mod.get_background(self.ctx.frequencies,
                                      self.ctx.params.elevation_model)
        
        # get all elevations from strategy (in radians)
        els = np.asarray(self.ctx.strategy_coords)[:,1]
        #add background to TOD
        #TODO: no background for Y-polarization
        self.ctx.tod_vx += bg_model(els)
    
    def __str__(self):
        return "Adding background to TOD"
