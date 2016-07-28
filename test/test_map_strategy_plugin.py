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

from ivy.utils.struct import Struct
from hide.plugins import map_strategy_plugin
from hide.strategy import CoordSpec
from hide.utils import parse_datetime


class TestMapStrategyPlugin(object):

    def test_map_strategies(self):
        durration = 10
        time_range = 5
        params = Struct(time_range = time_range,
                        strategy_step_size=1,
                        verbose=False
                        )
        ctx = Struct(params = params,
                     strategy_start = parse_datetime("2015-01-01-00:00:00"),
                     strategy=[CoordSpec(t, 0, 0, 0, 0) for t in xrange(durration)])
        
        plugin = map_strategy_plugin.Plugin(ctx)
        
        
        for idx, ctx in enumerate(plugin.getWorkload()):
            assert ctx is not None
            assert ctx.strategy_idx == idx
            assert ctx.strategy_coords is not None
            assert ctx.batch_start_date is not None
            assert len(ctx.strategy_coords) == time_range
        
        assert idx == (durration / time_range)-1