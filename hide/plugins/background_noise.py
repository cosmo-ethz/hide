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

from ivy.plugin.base_plugin import BasePlugin
from hide.utils.signal import noisegen
import importlib


class Plugin(BasePlugin):
    """
    Adds background noise to the time ordered data
    """

    def __call__(self):
        params = self.ctx.params
        size = self.ctx.tod_vx.shape
        if params.load_noise_template:
            mod = importlib.import_module(self.ctx.params.instrument)
            freq = self.ctx.frequencies
            wn_scale, cn_amp, cn_beta = mod.get_noise_params(freq)
            params.white_noise_scale = wn_scale
            params.color_noise_amp = cn_amp
            params.color_noise_beta = cn_beta 
        
        noise = get_noise(params.white_noise_scale, params.color_noise_amp,
                          params.color_noise_beta, size)
        
        self.ctx.tod_vx += noise
        #TODO: no noise for Y-polarization
#         self.ctx.tod_vy += noise
        
    def __str__(self):
        return "Add background noise"
    
def get_noise(scale, alpha, beta, size):
    wnoise = np.random.normal(scale=np.atleast_1d(scale).reshape(-1,1),
                              size=size)
    # only create colored noise if amplitude is greater than zero
    if np.any(alpha > 0):
        rnoise = noisegen(beta, size) * np.atleast_1d(alpha).reshape(-1,1)
        return wnoise + rnoise
    else:
        return wnoise