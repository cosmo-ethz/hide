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
Created on Feb 26, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import healpy as hp

from ivy.utils.struct import Struct

from hide.astro import static_gsm

class TestStaticGsm(object):
    
    def test_load_signal_normal(self):
        params = Struct(beam_nside=static_gsm.GSM_NSIDE)
        ctx = Struct(params = params)
        
        astro_signal = static_gsm.load_signal(ctx)
        assert astro_signal is not None
        assert hp.get_nside(astro_signal) == ctx.params.beam_nside
        
        
    def test_load_signal_rescaling(self):
        params = Struct(beam_nside = 2**6)
        ctx = Struct(params = params)
        astro_signal = static_gsm.load_signal(ctx)
        assert astro_signal is not None
        assert hp.get_nside(astro_signal) == ctx.params.beam_nside