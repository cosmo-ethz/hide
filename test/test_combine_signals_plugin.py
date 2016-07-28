# HIDE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# HIDE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with HIDE.  If not, see <http://www.gnu.org/licenses/>.


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
