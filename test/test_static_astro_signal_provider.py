# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 8, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import healpy as hp
import numpy as np

from ivy.utils.struct import Struct

from hide.astro import static


class TestStaticAstroSignalProvider(object):

    def test_load_signal(self):
        params = Struct(astro_flux=255, 
                        beam_nside=32)
        ctx = Struct(params = params,
                     )
        
        signal = static.load_signal(ctx)
        
        assert signal is not None
        assert len(signal) == hp.nside2npix(params.beam_nside)
        assert np.all(signal == params.astro_flux)