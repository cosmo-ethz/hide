# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 9, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from ivy.utils.struct import Struct
from hide.earth import horizon

class TestEarthSignalPlugin(object):

    def test_load_signal(self):
        params = Struct(beam_nside=2**4,
                        vmin=-np.pi/2,
                        vmax= np.pi/2,
                        fit_coeffs=[1],
                        log_base=1)
        
        ctx = Struct(params = params,
                     )
        
        earth_signal = horizon.load_signal(ctx)
        
        assert earth_signal is not None
        assert np.all(earth_signal==params.log_base)