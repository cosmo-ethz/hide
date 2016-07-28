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
Created on Dec 11, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from ivy.utils.struct import Struct
from hide.plugins import map_frequency_plugin


class TestMapStrategyPlugin(object):

    def test_map_frequencies(self):
        frequencies = np.arange(0, 10)
        beam_profiles = [None] * len(frequencies)
        beam_norms = range(len(frequencies))
        ctx = Struct(beam_profiles=beam_profiles,
                     beam_norms=beam_norms,
                     frequencies=frequencies)
        
        plugin = map_frequency_plugin.Plugin(ctx)
        
        for idx, ctx in enumerate(plugin.getWorkload()):
            assert ctx is not None
            assert ctx.frequency_idx == idx
            assert ctx.frequency is not None
            assert ctx.frequency == idx
            assert np.all(ctx.beam_profile == beam_profiles[idx])
            assert ctx.beam_norm == beam_norms[idx]
        
        assert idx == frequencies[-1]