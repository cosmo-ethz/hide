# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Sep 4, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from ivy.utils.struct import Struct
from hide.strategy import drift_scan
from hide.utils import parse_datetime

class TestDriftScanStrategy(object):
    
    def test_load_strategy(self):
        params = Struct(telescope_latitude = 47.344192,
                        telescope_longitude = 8.114368,
                        alt_delta = 3.5,
                        azimuth_pointing = 181,
                        altitude_start_pos = 41.0,
                        altitude_max_pos = 90.0,
                        strategy_step_size = 1,
                        )
        
        ctx = Struct(params=params,
                     strategy_start = parse_datetime("2015-01-01-00:00:00"),
                     strategy_end   = parse_datetime("2015-01-01-00:01:00"))
        
        strategy = drift_scan.load_strategy(ctx)
        
        assert len(strategy) == 60 / params.strategy_step_size