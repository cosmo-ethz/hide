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
Created on Mar 2, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals
from ivy.utils.struct import Struct

import numpy as np
from hide.spectrometer import callisto

def test_post_processing():
    
    tod_vx = np.random.uniform(1, 250, (100, 100))
    params = Struct(log_base = 10,
                    offset_baseline=10,
                    model_slope = 0,
                    model_sw = [0.],
                    model_fmin = 1,
                    model_fmax = 2,
                    model_nf = 1)
    ctx = Struct(params=params,
                 tod_vx=tod_vx,
                 frequencies = np.arange(100))
    
    callisto.apply_gain(ctx)
    
    assert np.allclose(np.log10(tod_vx)+params.offset_baseline, ctx.tod_vx)
    assert ctx.tod_vy is not None