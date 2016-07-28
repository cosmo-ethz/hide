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
Created on Nov 25, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
import healpy as hp

def load_signal(ctx):
    """
    Returns a constant signal
    
    :param ctx: context object containing params
    
    :returns earth_signal: healpy map with the signal
    """
    nside = ctx.params.beam_nside
    earth_signal = ctx.params.earth_signal_flux * np.ones(hp.nside2npix(nside), np.float32)
    
    return earth_signal