# Copyright (C) 2016 ETH Zurich, Institute for Astronomy

'''
Created on Mar 23, 2016

author: seehars
'''
from __future__ import print_function, division, absolute_import, unicode_literals
from hide.plugins.add_background import Plugin
from hide.strategy import CoordSpec
from ivy.utils.struct import Struct

import numpy as np
from mock import patch

class TestAddBackgroundPlugin(object):
    
    def test_add_background(self):
        
        tod_vx = np.random.uniform(1, 250, (100, 100))
        params = Struct(instrument = "hide.spectrometer.M9703A",
                        elevation_model = [1,0])
        freq = np.arange(100)
        els = np.linspace(0,np.pi/2,100)
#         deg_els = np.degrees(els)
        strat = [CoordSpec(0.,el,0.,0.,0.) for el in els]
        ctx = Struct(params=params,
                     tod_vx=tod_vx.copy(),
                     frequencies = freq,
                     strategy_coords = strat)
        with patch("numpy.loadtxt") as load_txt_mock:
            load_txt_mock.return_value = np.vstack([freq, freq]).T
            plugin = Plugin(ctx)
            plugin()
        
        bg = freq.reshape(-1, 1) * els
        assert np.allclose(tod_vx+bg, ctx.tod_vx)