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

from hide.utils import sphere

def load_signal(ctx):
    """
    Models effect of the horizon
    
    :param ctx: context object containing params
    
    :returns earth_signal: healpy map with the signal
    """
    nside = ctx.params.beam_nside
    idx = np.arange(hp.nside2npix(nside))
    thetas, _ = hp.pix2ang(nside, idx)
    dec = sphere.theta2dec(thetas)
    
    min_mask = (dec<ctx.params.vmin) 
    max_mask = (dec>ctx.params.vmax)
    mask = min_mask | max_mask
    earth_signal = np.zeros(hp.nside2npix(nside))
    
    fit = np.poly1d(ctx.params.fit_coeffs)
    earth_signal[~mask] = fit(dec[~mask])
    earth_signal[min_mask] = fit(ctx.params.vmin)
    earth_signal[max_mask] = fit(ctx.params.vmax)
    earth_signal[:] = ctx.params.log_base**earth_signal
        
    return earth_signal
