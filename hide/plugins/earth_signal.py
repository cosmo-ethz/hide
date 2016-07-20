# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 8, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import importlib

from ivy.plugin.base_plugin import BasePlugin

earth_signal = None

class Plugin(BasePlugin):

    def __call__(self):
        
        global earth_signal
        if earth_signal is None:
            #load module
            mod = importlib.import_module(self.ctx.params.earth_signal_provider)
            #delegate loading of signal
            earth_signal = mod.load_signal(self.ctx)
            
        self.ctx.earth_signal = earth_signal


    def __str__(self):
        return "Applying earth signals"