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

from ivy.plugin.base_plugin import BasePlugin


class Plugin(BasePlugin):
    """
    Combines the different signals by convolving the beam profile with the input signals
    """

    def __call__(self):
        
        signals = []
        beam_profile = self.ctx.beam_profile
        
        combined_signals = self.ctx.astro_signal + self.ctx.earth_signal
        
        # TODO: factor 1/2 for polarization is now put in here
        normalization = .5 * self.ctx.beam_norm
        for beam in self.ctx.beams:
            pixel_idxs = beam.pixel_idxs
            
            beam_response = beam_profile(beam.dec, beam.ra)
            signal = (beam_response * combined_signals[pixel_idxs]).sum()
            
            signals.append(normalization * signal)
        
        self.ctx.signals = signals
    
    def __str__(self):
        return "Combine signals"