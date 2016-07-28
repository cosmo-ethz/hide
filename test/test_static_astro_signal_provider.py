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

import healpy as hp
import numpy as np

from ivy.utils.struct import Struct

from hide.astro import static


class TestStaticAstroSignalProvider(object):

    def test_load_signal(self):
        params = Struct(astro_flux=255, 
                        beam_nside=32)
        ctx = Struct(params = params,
                     )
        
        signal = static.load_signal(ctx)
        
        assert signal is not None
        assert len(signal) == hp.nside2npix(params.beam_nside)
        assert np.all(signal == params.astro_flux)