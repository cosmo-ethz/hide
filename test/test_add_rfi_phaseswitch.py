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
Created on Mar 26, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from ivy.utils.struct import Struct
from hide.plugins import add_rfi_phaseswitch
from hide.strategy import CoordSpec
from datetime import datetime

class TestAddRFIPhaseswitchPlugin(object):
    
    def test_add_rfi_phaseswitch(self):
        
        nf = 300
        nt = 600
        tod = np.zeros((nf, nt))
        
        wn = np.arange(nf) + 1
        frac = .2 * np.ones(nf)
        Amax = 10 * wn
        
        params = Struct(white_noise_scale = wn, rfiamplitude = Amax, rfideltaf = 1,
                        rfideltat = 1, rfifrac = frac, load_rfi_template = False,
                        rfiexponent = 1, rfienhance = 1)
        
        strategy = [CoordSpec(t,0,0,0,0) for t in range(nt)]
        strategy_start = datetime(2016,1,1)
        ctx = Struct(params = params, tod_vx = tod.copy(), frequencies = wn, strategy_coords = strategy,
                     strategy_start = strategy_start)
        
        plugin = add_rfi_phaseswitch.Plugin(ctx)
        assert np.allclose(plugin.getTime(), np.arange(nt)/60./60.)

        plugin()
        
        assert np.sum(ctx.tod_vx) != 0
        assert np.all(ctx.tod_vx == ctx.tod_vx_rfi)
        
        ctx.params.rfiday = (3.0,23.0)
        ctx.params.rfidamping = 0.0
        ctx.tod_vx = tod
        plugin = add_rfi_phaseswitch.Plugin(ctx)
        plugin()
        assert np.isclose(np.sum(ctx.tod_vx), 0)
        
    def test_getDayNightMask(self):
        rfiday = (1.0, 23.0)
        time = np.array([0.2, 1.0, 2.0])
        assert np.all(add_rfi_phaseswitch.getDayNightMask(rfiday, time) == [False, False, True])