# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 9, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from ivy.utils.struct import Struct
from hide.plugins import combine_signals
from hide.beam import ResponseSpec


class TestCombineSignalsPlugin(object):

    def test_combine_signal(self):
        beam = ResponseSpec(np.arange(5), np.ones(5), np.ones(5))
        beam_profile = lambda theta, phi: np.array(1)
        
        earth_signal = np.zeros(len(beam.pixel_idxs))
        astro_signal = np.zeros(len(beam.pixel_idxs))
        
        time_steps = 5
        
        ctx = Struct(beams = [beam for _ in range(time_steps)],
                     earth_signal = earth_signal,
                     astro_signal = astro_signal,
                     beam_profile = beam_profile,
                     beam_norm = 1.0)
        
        plugin = combine_signals.Plugin(ctx)
        plugin()
        
        assert ctx.signals is not None
        assert len(ctx.signals) == time_steps
