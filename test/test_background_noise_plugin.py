# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 9, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from ivy.utils.struct import Struct
from hide.plugins import background_noise
import pytest
from hide.config.bleien import load_noise_template

class TestBackgroundNoisePlugin(object):

    def test_background_noise(self):
        n_time = 1000
        frequencies = 2000
        params = Struct(white_noise_scale=1,
                        color_noise_amp=0.00001,
                        color_noise_beta=0,
                        load_noise_template=False)
        ctx = Struct(params = params, 
                     tod_vx = np.zeros((frequencies, n_time)),
                     tod_vy = np.zeros((frequencies, n_time)))
        
        plugin = background_noise.Plugin(ctx)
        plugin()
        
        assert ctx.tod_vx is not None
        
        mean, std = np.mean(ctx.tod_vx), np.std(ctx.tod_vx)

        assert np.allclose(mean, 0, atol=1e-2)
        assert np.allclose(std, params.white_noise_scale, atol=1e-2)

