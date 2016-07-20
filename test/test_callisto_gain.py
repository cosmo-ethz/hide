# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Mar 2, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals
from ivy.utils.struct import Struct

import numpy as np
from hide.spectrometer import callisto

def test_post_processing():
    
    tod_vx = np.random.uniform(1, 250, (100, 100))
    params = Struct(log_base = 10,
                    offset_baseline=10,
                    model_slope = 0,
                    model_sw = [0.],
                    model_fmin = 1,
                    model_fmax = 2,
                    model_nf = 1)
    ctx = Struct(params=params,
                 tod_vx=tod_vx,
                 frequencies = np.arange(100))
    
    callisto.apply_gain(ctx)
    
    assert np.allclose(np.log10(tod_vx)+params.offset_baseline, ctx.tod_vx)
    assert ctx.tod_vy is not None