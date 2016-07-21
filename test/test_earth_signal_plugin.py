# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 9, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from ivy.utils.struct import Struct
from hide.plugins import earth_signal

class TestEarthSignalPlugin(object):

    def test_load_signal(self):
        params = Struct(beam_nside=32,
                        earth_signal_provider="hide.earth.constant",
                        earth_signal_flux=1)
        
        ctx = Struct(params = params,
                     )
        
        earth_signal.earth_signal = None
        plugin = earth_signal.Plugin(ctx)
        plugin()
        
        assert ctx.earth_signal is not None
        assert np.all(ctx.earth_signal==params.earth_signal_flux)