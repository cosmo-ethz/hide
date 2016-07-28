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
Created on Sep 14, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from ivy.utils.struct import Struct
from hide.plugins import clean_up

class TestCleanupPlugin(object):
    
    
    def test_clean_up(self):
        ctx = Struct(tod_vx = np.zeros((1,1)),
                     tod_vy = np.zeros((1,1)),
                     frequencies = np.zeros((1,1)),
                     strategy_coords = [(1,2,3,4,5)],
                     beams = [(1,2,3,4,5)],
                     tod_vx_rfi = np.ones((1,1)) 
                     )
        
        plugin = clean_up.Plugin(ctx)
        plugin()
        
        assert not ctx.has_key("tod_vx")
        assert not ctx.has_key("tod_vy")
        assert not ctx.has_key("frequencies")
        assert not ctx.has_key("strategy_coords")
        assert not ctx.has_key("beams")
        assert not ctx.has_key("tod_vx_rfi")
        