# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Jan 12, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from scipy import stats
import numpy as np
from hide.utils import signal

class TestNoiseGen(object):

    def test_white_noise_gen(self):
        N=(1, 2**13)
        out = signal.noisegen(N=N, beta=0)
        out = out * 1./np.std(out) #rescale for KS(norm(0,1))
        assert out is not None
        assert out.shape == N
        D, p = stats.kstest(out[0], "norm")
        
        assert D < 0.015
