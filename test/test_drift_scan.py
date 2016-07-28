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
Created on Sep 4, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from ivy.utils.struct import Struct
from hide.strategy import drift_scan
from hide.utils import parse_datetime

class TestDriftScanStrategy(object):
    
    def test_load_strategy(self):
        params = Struct(telescope_latitude = 47.344192,
                        telescope_longitude = 8.114368,
                        alt_delta = 3.5,
                        azimuth_pointing = 181,
                        altitude_start_pos = 41.0,
                        altitude_max_pos = 90.0,
                        strategy_step_size = 1,
                        )
        
        ctx = Struct(params=params,
                     strategy_start = parse_datetime("2015-01-01-00:00:00"),
                     strategy_end   = parse_datetime("2015-01-01-00:01:00"))
        
        strategy = drift_scan.load_strategy(ctx)
        
        assert len(strategy) == 60 / params.strategy_step_size