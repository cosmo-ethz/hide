# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Mar 2, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals
from hide.plugins.apply_gain import Plugin
from ivy.utils.struct import Struct

import numpy as np
from mock import patch

class TestApplyGainPlugin(object):
    
    def test_apply_gain(self):
        freq_no = 100
        tod_vx = np.random.uniform(1, 250, (freq_no, 10))
        params = Struct(instrument = "hide.spectrometer.M9703A")
        freq = np.arange(freq_no)
        gain = np.arange(freq_no)
        ctx = Struct(params=params,
                     tod_vx=tod_vx.copy(),
                     frequencies = freq)
        with patch("numpy.loadtxt") as load_txt_mock:
            load_txt_mock.return_value = np.vstack([freq, gain]).T
            plugin = Plugin(ctx)
            plugin()

        assert np.allclose(tod_vx*gain.reshape(-1,1), ctx.tod_vx)