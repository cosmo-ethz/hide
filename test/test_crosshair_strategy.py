# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Jan 12, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

from ivy.utils.struct import Struct
from hide.strategy import crosshair
from hide.utils import parse_datetime

class TestCrosshairStrategy(object):
    
    def test_load_strategy(self):
        params = Struct(telescope_latitude = 47.344192,
                        telescope_longitude = 8.114368,
                        strategy_step_size = 1)
        
        ctx = Struct(params = params,
                     strategy_start = parse_datetime("2015-01-01-00:00:00"),
                     strategy_end   = parse_datetime("2015-01-01-00:00:10"))
        
        strategy = crosshair.load_strategy(ctx)
        
        assert strategy is not None
        assert len(strategy) == 10
        
        for coord in strategy:
            assert 0 <= coord.alt <= 2 * np.pi
            assert 0 <= coord.az  <= 2 * np.pi
            