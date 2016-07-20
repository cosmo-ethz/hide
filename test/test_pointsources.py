# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Apr 26, 2016

author: seehars
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
import healpy as hp
from ivy.utils.struct import Struct
from hide.plugins import add_point_sources

class TestAddPointsourcesPlugin(object):
    
    def test_add_point_sources(self):
        
        freq = 1.0
        nside = 16
        params = Struct(beam_nside = nside)
        
        Map = np.zeros(hp.nside2npix(nside))
        ctx = Struct(params = params, frequency = freq, astro_signal = Map)
        
        plugin = add_point_sources.Plugin(ctx)
        plugin()
        assert np.any(Map != 0.0)
        
