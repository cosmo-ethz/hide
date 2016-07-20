# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 11, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from ivy.utils.struct import Struct
from hide.plugins import map_strategy_plugin
from hide.strategy import CoordSpec
from hide.utils import parse_datetime


class TestMapStrategyPlugin(object):

    def test_map_strategies(self):
        durration = 10
        time_range = 5
        params = Struct(time_range = time_range,
                        strategy_step_size=1,
                        verbose=False
                        )
        ctx = Struct(params = params,
                     strategy_start = parse_datetime("2015-01-01-00:00:00"),
                     strategy=[CoordSpec(t, 0, 0, 0, 0) for t in xrange(durration)])
        
        plugin = map_strategy_plugin.Plugin(ctx)
        
        
        for idx, ctx in enumerate(plugin.getWorkload()):
            assert ctx is not None
            assert ctx.strategy_idx == idx
            assert ctx.strategy_coords is not None
            assert ctx.batch_start_date is not None
            assert len(ctx.strategy_coords) == time_range
        
        assert idx == (durration / time_range)-1