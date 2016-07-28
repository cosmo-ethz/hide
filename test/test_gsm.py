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

import pytest
import healpy as hp
import numpy as np

from ivy.utils.struct import Struct
from pkg_resources import resource_filename


from hide.astro import gsm
import os
import hide

GSM_NSIDE = 64

class TestGsm(object):
    
    def test_frequency_range(self):
        params = Struct(beam_nside = GSM_NSIDE)
        ctx = Struct(params = params)
        
        ctx.frequency = 0
        with pytest.raises(AssertionError):
            gsm.load_signal(ctx)
            
        ctx.frequency = 979
        with pytest.raises(AssertionError):
            gsm.load_signal(ctx)
            
        ctx.frequency = 1281
        with pytest.raises(AssertionError):
            gsm.load_signal(ctx)
            
        ctx.frequency = 1286
        with pytest.raises(AssertionError):
            gsm.load_signal(ctx)
            
    def test_load_signal(self):
        params = Struct(beam_nside = GSM_NSIDE)
        ctx = Struct(params = params)
        
        ctx.frequency = 980.0
        astro_signal = gsm.load_signal(ctx)
        assert astro_signal is not None
        assert hp.get_nside(astro_signal) == ctx.params.beam_nside

        root_file_path = resource_filename(hide.__name__, gsm.GSM_FILE_PATH)        
        file_path = os.path.join(root_file_path, str(params.beam_nside), "gsm_%s.fits"%(ctx.frequency))
        gsm_map = hp.read_map(file_path)
        assert np.all(gsm_map == astro_signal)
        
        ctx.frequency = 1000.0
        astro_signal = gsm.load_signal(ctx)
        assert astro_signal is not None
        assert hp.get_nside(astro_signal) == ctx.params.beam_nside
        
        file_path = os.path.join(root_file_path, str(params.beam_nside), "gsm_%s.fits"%(ctx.frequency))
        gsm_map = hp.read_map(file_path)
        assert np.all(gsm_map == astro_signal)
        
        ctx.frequency = 1280.0
        astro_signal = gsm.load_signal(ctx)
        assert astro_signal is not None
        assert hp.get_nside(astro_signal) == ctx.params.beam_nside
        
        file_path = os.path.join(root_file_path, str(params.beam_nside), "gsm_%s.fits"%(ctx.frequency))
        gsm_map = hp.read_map(file_path)
        assert np.all(gsm_map == astro_signal)
        
    def test_load_signal_interp(self):
        params = Struct(beam_nside = GSM_NSIDE)
        ctx = Struct(params = params)
        
        ctx.frequency = 982.5
        astro_signal = gsm.load_signal(ctx)
        assert astro_signal is not None
        assert hp.get_nside(astro_signal) == ctx.params.beam_nside
        
        root_file_path = resource_filename(hide.__name__, gsm.GSM_FILE_PATH)
        file_path = os.path.join(root_file_path, str(params.beam_nside), "gsm_%s.fits"%(980.0))
        gsm_map1 = hp.read_map(file_path)
        file_path = os.path.join(root_file_path, str(params.beam_nside), "gsm_%s.fits"%(985.0))
        gsm_map2 = hp.read_map(file_path)
        
        gsm_map = (gsm_map1 + gsm_map2) / 2
        
        assert np.all(gsm_map == astro_signal)

    def test_load_signal_rescale(self):
        params = Struct(beam_nside = 2**6)
        ctx = Struct(params = params)
        
        ctx.frequency = 980
        astro_signal = gsm.load_signal(ctx)
        assert astro_signal is not None
        assert hp.get_nside(astro_signal) == ctx.params.beam_nside
