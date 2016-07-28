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
Created on Dec 11, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from ivy.utils.struct import Struct
from hide.plugins import reduce_frequency_plugin
import pytest

@pytest.skip("currently not used")
class TestReduceSignalsPlugin(object):

    def test_reduce(self):
        tod_vx = np.ones(10)
        ctx = Struct(tod_vx = tod_vx)
        
        ctx_count = 5
        ctxList = [ctx.copy() for _ in xrange(ctx_count)]
        
        plugin = reduce_frequency_plugin.Plugin(ctx)
        plugin.reduce(ctxList)
        
        assert ctx.tod_vx is not None
        assert ctx.tod_vx.shape == (ctx_count, 10)