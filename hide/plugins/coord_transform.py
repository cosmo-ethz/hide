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
from hide.beam import ResponseSpec

class Plugin(BasePlugin):
    """
    Applies the coordination transformation to the beam profile by rotating 
    the beam response on the sky sphere according to the defined scanning strategy 
    """

    def __call__(self):
        beam_spec = self.ctx.beam_spec
        nside = self.ctx.params.beam_nside
        beams = []
        for coord in self.ctx.strategy_coords:
            coord_ra, coord_dec = coord[3], coord[4]
            
            #rotate to scanning strategy pos
            thetas, phis = np.meshgrid(sphere.dec2theta(beam_spec.dec), sphere.ra2phi(beam_spec.ra))
            rotator = hp.Rotator(rot=[0, -coord_dec,  0], deg=False)
            rthetas, rphis = rotator(thetas.flatten(), phis.flatten())
            rphis += coord_ra
            
            field_idx = np.unique(hp.ang2pix(nside, rthetas, rphis).T)
            rthetas, rphis = hp.pix2ang(nside, field_idx)
            
            # recenter around (0/0)
            rphis -= coord_ra
            cthetas, cphis = rotator(rthetas, rphis, inv=True)
            decs = sphere.theta2dec(cthetas)
            ras = sphere.phi2ra(cphis)
            
            beam = ResponseSpec(field_idx, ras, decs)
            beams.append(beam)
            
            plot=False
            if plot:
                plot_beam(beam_spec, coord_ra, coord_dec, rphis, rthetas, ras, decs)
                
        self.ctx.beams = beams

        
    def __str__(self):
        return "Coord transformation"
    
def plot_beam(beam_spec, coord_ra, coord_dec, rphis, rthetas, ras, decs):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12,5))
    plt.suptitle("RA: {0:>.4f}, DEC: {1:>.4f}".format(coord_ra, coord_dec))
    plt.subplot(121)
    plt.scatter(rphis, rthetas, 1)
    plt.scatter(sphere.ra2phi(coord_ra), sphere.dec2theta(coord_dec), 10)
    plt.xlabel("phi / ra")
    plt.ylabel("theta / dec")
     
    plt.subplot(122)
    plt.scatter(ras, decs, 1)
    plt.scatter(0, 0, 10)
    plt.scatter(beam_spec.dec[-1], beam_spec.ra[-1], 5)
    plt.scatter(beam_spec.dec[0], beam_spec.ra[-1], 5)
    plt.scatter(beam_spec.dec[-1], beam_spec.ra[0], 5)
    plt.scatter(beam_spec.dec[0], beam_spec.ra[0], 5)

    plt.xlabel("phi / ra")
    plt.ylabel("theta / dec")
    plt.show()   