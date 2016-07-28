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

import importlib
import numpy as np
import healpy as hp

from ivy.plugin.base_plugin import BasePlugin
from hide.beam import BeamSpec


class Plugin(BasePlugin):
    """
    Delegates the loading process to the beam profile provider 
    """

    def __call__(self):
        #load module
        mod = importlib.import_module(self.ctx.params.beam_profile_provider)
        
        #delegate loading of profile
        
        params = self.ctx.params
        #setting up angular grid
        beam_area = np.radians(params.beam_elevation) * np.radians(params.beam_azimut) # [rad]
        pixel_area = hp.nside2pixarea(params.beam_nside, degrees=False)
        pixels = np.floor(np.sqrt(beam_area / pixel_area))
        pixels = pixels if pixels%2==1 else pixels+1
        
        pixel_size = hp.max_pixrad(params.beam_nside)
        theta = (np.linspace(0, pixels, pixels*2+1)-pixels/2)*(pixel_size)
        phi = theta
        
        beam_spec = BeamSpec(phi, theta, pixels**2)
        frequencies = np.arange(params.beam_frequency_min, params.beam_frequency_max, params.beam_frequency_pixscale)
        
        beam_profiles, beam_norms = mod.load_beam_profile(beam_spec, frequencies, self.ctx.params)
        
        self.ctx.beam_spec = beam_spec
        self.ctx.frequencies = frequencies
        self.ctx.beam_profiles = beam_profiles
        self.ctx.beam_norms = beam_norms
    
    def __str__(self):
        return "Load beam profile"