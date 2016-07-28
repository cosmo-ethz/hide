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
Created on Dec 8, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
import healpy as hp

from ivy.plugin.base_plugin import BasePlugin

from hide.utils import sphere
from hide.utils import quaternion as qu
from hide.beam import ResponseSpec

class Plugin(BasePlugin):
    """
    Applies the coordination transformation to the beam profile by rotating 
    the beam response on the sky sphere according to the defined scanning strategy 
    """

    def __call__(self):
        beam_spec = self.ctx.beam_spec
        
        nside = self.ctx.params.beam_nside
        idx = np.arange(hp.nside2npix(nside))
        thetas, phis = hp.pix2ang(nside, idx)
        tree = sphere.ArcKDTree(thetas, phis)
        
        beams = []
        for coord in self.ctx.strategy_coords:
            coord_ra, coord_dec = coord[3], coord[4]
            
            #rotate to scanning strategy pos
            _, field_idx = tree.query(sphere.dec2theta(coord_dec), sphere.ra2phi(coord_ra), beam_spec.pixels)
            vec = tree.tree.data[field_idx]

            # recenter around (0/0)
            q1 = qu.vecquad(0, 1, 0, -coord_dec)
            q2 = qu.vecquad(0, 0, 1, coord_ra)
            q = qu.mult(q2, q1)
            rotator = qu.VecRotator(q)
            cthetas, cphis = rotator(vec, inverse=True)
            
            decs = sphere.theta2dec(cthetas)
            ras = sphere.phi2ra(cphis)
            
            beam = ResponseSpec(field_idx, ras, decs)
            beams.append(beam)
            
            plot=False
            if plot:
                from hide.plugins import coord_transform
                rthetas, rphis = sphere.vec2dir(vec)
                coord_transform.plot_beam(beam_spec, coord_ra, coord_dec, rphis, rthetas, ras, decs)
                
        self.ctx.beams = beams

        
    def __str__(self):
        return "Coord transformation"