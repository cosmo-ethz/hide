# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 8, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

from ivy.plugin.base_plugin import BasePlugin
from hide.utils import parse_datetime


class Plugin(BasePlugin):
    """
    Initialize  ..,
    
    """

    def __call__(self):
        np.random.seed(self.ctx.params.seed)
        self.ctx.strategy_start = parse_datetime(self.ctx.params.strategy_start)
        self.ctx.strategy_end   = parse_datetime(self.ctx.params.strategy_end)
                                                    
    def __str__(self):
        return "Initialize"