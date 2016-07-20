# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Feb 27, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from ivy.plugin.base_plugin import BasePlugin

import importlib

class Plugin(BasePlugin):
    """
    Transform the temperature based (Kelvin) TOD into ADU by applying a
    spectrometer specific gain
    """

    def __call__(self):
        #load module
        mod = importlib.import_module(self.ctx.params.instrument)
        
        #delegate loading of gain per frequency
        gain = mod.get_gain(self.ctx.frequencies)
        
        #apply gain to TOD
        #TODO: no gain for Y-polarization
#         self.ctx.gain = gain
        self.ctx.tod_vx *= gain.reshape(-1, 1)
    
    def __str__(self):
        return "Applying gain to TOD"