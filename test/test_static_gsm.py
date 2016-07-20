# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Feb 26, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import healpy as hp

from ivy.utils.struct import Struct

from hide.astro import static_gsm

class TestStaticGsm(object):
    
    def test_load_signal_normal(self):
        params = Struct(beam_nside=static_gsm.GSM_NSIDE)
        ctx = Struct(params = params)
        
        astro_signal = static_gsm.load_signal(ctx)
        assert astro_signal is not None
        assert hp.get_nside(astro_signal) == ctx.params.beam_nside
        
        
    def test_load_signal_rescaling(self):
        params = Struct(beam_nside = 2**6)
        ctx = Struct(params = params)
        astro_signal = static_gsm.load_signal(ctx)
        assert astro_signal is not None
        assert hp.get_nside(astro_signal) == ctx.params.beam_nside