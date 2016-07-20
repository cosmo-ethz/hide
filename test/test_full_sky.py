# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Jan 12, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
import healpy as hp

from ivy.utils.struct import Struct
from hide.strategy import full_sky
from hide.utils import parse_datetime

class TestFullSkyStrategy(object):
    
    def test_load_strategy(self):
        params = Struct(telescope_latitude = 47.344192,
                        telescope_longitude = 8.114368,
                        beam_nside = 32,
                        strategy_step_size = 1)
        
        ctx = Struct(params = params,
                     strategy_start = parse_datetime("2015-01-01-00:00:00"),
                     )
        
        strategy = full_sky.load_strategy(ctx)
        
        assert strategy is not None
        assert len(strategy) == hp.nside2npix(params.beam_nside)
        
        for coord in strategy:
            assert 0 <= coord.alt <= 2 * np.pi
            assert 0 <= coord.az  <= 2 * np.pi
            