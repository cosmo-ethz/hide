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
        
