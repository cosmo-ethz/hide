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
Created on Jan 12, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

from ivy.utils.struct import Struct
from hide.plugins import qu_opt_coord_transform
from hide.beam import BeamSpec
from hide.strategy import CoordSpec

import healpy as hp
from hide.utils import sphere


class TestQuOptCoordTransformPlugin():
    
    def test_transform(self):
        nside = 2**4
        
        params = Struct(beam_nside = nside)
        
        strategy_coord = CoordSpec(0, 0, 0, 0, 0)
        
        beam_size = 0.041
        beam_spec = BeamSpec([beam_size], [beam_size], 2)
        
        time_steps = 2
        
        idx = np.arange(hp.nside2npix(nside))
        thetas, phis = hp.pix2ang(nside, idx)
        tree = sphere.ArcKDTree(thetas, phis)
        
        ctx = Struct(params = params,
                     strategy_coords = [strategy_coord for _ in range(time_steps)],
                     beam_spec = beam_spec,
                     arc_tree = tree)
        
        plugin = qu_opt_coord_transform.Plugin(ctx)
        plugin()
        
        assert ctx.beams is not None
        assert len(ctx.beams) == time_steps
        
