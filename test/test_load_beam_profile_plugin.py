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

from ivy.utils.struct import Struct
from hide.plugins import load_beam_profile

class TestLoadBeamProfilePlugin(object):

    def test_load_profile(self):
        params = Struct(beam_profile_provider = "hide.beam.top_hat",
                        beam_elevation = 21,
                        beam_azimut = 21,
                        beam_frequency_min = 10,
                        beam_frequency_max = 17,
                        beam_frequency_pixscale = 1,
                        beam_pixscale = 1,
                        beam_response = 1,
                        beam_nside = 2**6)
        
        ctx = Struct(params = params,)
        
        plugin = load_beam_profile.Plugin(ctx)
        plugin()
        
        assert ctx.beam_profiles is not None
        assert len(ctx.beam_profiles) == 7
        assert ctx.frequencies is not None
        assert len(ctx.frequencies) == 7
        assert ctx.beam_norms is not None 
        assert len(ctx.beam_norms) == 7
