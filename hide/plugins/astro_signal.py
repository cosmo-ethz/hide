# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 8, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import importlib
from ivy.plugin.base_plugin import BasePlugin

astro_signal_cache = {}

class Plugin(BasePlugin):

    def __call__(self):
        
        global astro_signal_cache
        try:
            astro_signal = astro_signal_cache[self.ctx.frequency]
        except KeyError:
            #load module
            mod = importlib.import_module(self.ctx.params.astro_signal_provider)
            #delegate loading of signal
            astro_signal = mod.load_signal(self.ctx)
            
            if self.ctx.params.cache_astro_signals:
                astro_signal_cache[self.ctx.frequency] = astro_signal
            
        self.ctx.astro_signal = astro_signal

    
    def __str__(self):
        return "Applying astro signals"