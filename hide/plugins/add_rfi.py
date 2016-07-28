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
from scipy import stats

class Plugin(BasePlugin):
    """
    Adds RFI to the time ordered data
    """

    def __call__(self):
        params = self.ctx.params
        fit_sigma_freq = np.poly1d(params.coeff_freq)
        fit_sigma_time = np.poly1d(params.coeff_time)

        max_rfi_count = (self.ctx.tod_vx.shape[1] * self.ctx.params.strategy_step_size) / 3600 * params.max_rfi_count
        
        rfi_count = np.floor(np.random.uniform(1, max_rfi_count)).astype(np.int) 
        
        for rfi_idx in range(rfi_count):
            amp = np.fabs(stats.lognorm.rvs(1, loc=params.amp_loc, scale=params.amp_scale, size=1))
            sigma_freq = fit_sigma_freq(amp)
            sigma_time = fit_sigma_time(amp)
#             print("amp, sigma_freq, sigma_time", amp, sigma_freq, sigma_time)
             
            grid_x = np.arange(-params.sigma_range * sigma_time, params.sigma_range * sigma_time)
            grid_y = np.arange(-params.sigma_range * sigma_freq, params.sigma_range * sigma_freq)
            X,Y = np.meshgrid(grid_x,grid_y)
             
#             time_offset = np.random.normal(0, 1)
            time_offset = np.random.uniform(-params.sigma_range, params.sigma_range)
#             time_offset = sigma_range if np.fabs(time_offset) > sigma_range else time_offset
            Z = gaussian(amp, time_offset * sigma_time, 0, sigma_time, sigma_freq)(X,Y)
             
            pos_time = np.floor(np.random.uniform(0, self.ctx.tod_vx.shape[1] - 2 * params.sigma_range * sigma_time))
            pos_freq = np.floor(np.random.uniform(0, self.ctx.tod_vx.shape[0] - 2 * params.sigma_range * sigma_freq))
             
            if pos_time >= 0 and pos_freq >= 0:
                self.ctx.tod_vx[pos_freq: pos_freq + Z.shape[0], pos_time: pos_time + Z.shape[1]] += Z


        #constant
        for rfi_freq in params.rfi_freqs:
            amp = np.random.uniform(params.min_amp, params.max_amp)
#             print("amp", amp)
            scales1 = amp * np.exp(-np.arange(params.rfi_width-1, 0, -1) * 1.0)
            scales2 = amp * np.exp(-np.arange(0, params.rfi_width,  1) * 0.8)
            scales = np.append(scales1, scales2)
#             print("scales", scales)
            for i, rfi_pos in enumerate(np.arange(params.rfi_width-1, -params.rfi_width, -1)):
                scale = scales[i]
                rfi = np.random.normal(scale, scale, self.ctx.tod_vx.shape[1])
                self.ctx.tod_vx[rfi_freq - rfi_pos, : ] += rfi

    
    def __str__(self):
        return "Add RFI"
    
def gaussian(height, center_x, center_y, width_x, width_y):
    """Returns a gaussian function with the given parameters"""
    width_x = float(width_x)
    width_y = float(width_y)
    return lambda x,y: height*np.exp(
                -(((center_x-x)/width_x)**2+((center_y-y)/width_y)**2)/2)
