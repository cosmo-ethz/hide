# Copyright (C) 2014 ETH Zurich, Institute for Astronomy
 
'''
Created on Dec 9, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from ivy.utils.struct import Struct
from hide.plugins import scanning_strategy
from hide.utils import parse_datetime

class TestScanningStrategyPlugin(object):

    def test_load_strategy(self):
        params = Struct(scanning_strategy_provider = "hide.strategy.center",
                        strategy_step_size = 1)
        
        ctx = Struct(params = params,
                     strategy_start = parse_datetime("2015-01-01-00:00:00"),
                     strategy_end   = parse_datetime("2015-01-01-00:00:10"))
        
        plugin = scanning_strategy.Plugin(ctx)
        plugin()
        
        assert ctx.strategy is not None
        assert len(ctx.strategy) == 10