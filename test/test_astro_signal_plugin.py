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
from hide.plugins import astro_signal

class TestAstroSignalPlugin(object):

    def test_load_signal(self):
        astro_flux=1
        params = Struct(astro_signal_provider = "hide.astro.static",
                        beam_nside = 32,
                        astro_flux=astro_flux,
                        cache_astro_signals = False)
        
        ctx = Struct(params = params,
                     strategy_idx = 0,
                     frequency=0)
        
        plugin = astro_signal.Plugin(ctx)
        plugin()
        assert ctx.astro_signal is not None
        assert np.all(ctx.astro_signal == params.astro_flux)
        
        #same frequency
        plugin()
        assert ctx.astro_signal is not None
        assert np.all(ctx.astro_signal == params.astro_flux)
        
        
        ctx.frequency = 1
        astro_flux = 2
        ctx.params.astro_flux = astro_flux 
        plugin = astro_signal.Plugin(ctx)
        plugin()
        assert ctx.astro_signal is not None
        assert np.all(ctx.astro_signal == params.astro_flux)
