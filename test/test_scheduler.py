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
Created on Mar 29, 2016

author: seehars
'''
from __future__ import print_function, division, absolute_import, unicode_literals
from ivy.utils.struct import Struct

import numpy as np
from hide.strategy import scheduler
import os
from hide.utils import parse_datetime

ROOT_PATH = os.path.join(os.path.dirname(__file__), "res")

def test_scheduler():
    
    # constant elevation model
    params = Struct(scheduler_file = os.path.join(ROOT_PATH,
                                                  "schedule.txt"),
                    strategy_step_size = 60,
                    time_range = 15*60,
                    telescope_latitude = 47.344192,
                    telescope_longitude = 8.114368)
    
    strategy_start = parse_datetime("2015-12-21-02:00:00")
    strategy_end   = parse_datetime("2015-12-22-09:00:00")

    ctx = Struct(params=params,
                 strategy_start=strategy_start,
                 strategy_end=strategy_end)
    
    strategy = scheduler.load_strategy(ctx)
    
    assert len(ctx.calibration["2015-12-22"]) == 1
    assert len(strategy) == int((strategy_end - strategy_start).total_seconds())/60
    assert strategy[0].az == np.radians(200.0)
    assert strategy[-1].az == np.radians(56.1684772811)
    assert strategy[0].alt == np.radians(36.0)
    assert strategy[-1].alt == np.radians(25.0529699511)