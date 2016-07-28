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
Created on Dec 9, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from ivy.utils.struct import Struct
from hide.earth import horizon

class TestEarthSignalPlugin(object):

    def test_load_signal(self):
        params = Struct(beam_nside=2**4,
                        vmin=-np.pi/2,
                        vmax= np.pi/2,
                        fit_coeffs=[1],
                        log_base=1)
        
        ctx = Struct(params = params,
                     )
        
        earth_signal = horizon.load_signal(ctx)
        
        assert earth_signal is not None
        assert np.all(earth_signal==params.log_base)