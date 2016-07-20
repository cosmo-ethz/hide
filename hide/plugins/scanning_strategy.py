# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 8, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import importlib

from ivy.plugin.base_plugin import BasePlugin


class Plugin(BasePlugin):

    def __call__(self):
        #load module
        mod = importlib.import_module(self.ctx.params.scanning_strategy_provider)
        
        #delegate loading of strategy
        self.ctx.strategy = mod.load_strategy(self.ctx)
            
    def __str__(self):
        return "Load scanning strategy"