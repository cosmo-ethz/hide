# Copyright (C) 2016 ETH Zurich, Institute for Astronomy

'''
Created on Mar 29, 2016

author: seehars
'''
from __future__ import print_function, division, absolute_import, unicode_literals
from ivy.utils.struct import Struct

import numpy as np
from hide.strategy import scheduler_virtual
import os
from hide.utils import parse_datetime
from hide.astro import gsm_point_src

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
    
    strategy = scheduler_virtual.load_strategy(ctx)
    
    assert len(ctx.calibration["2015-12-22"]) == 1
    calib_src = ctx.calibration["2015-12-22"][0]
    assert calib_src.src == "CygA"
    assert len(strategy) == int((strategy_end - strategy_start).total_seconds())/60
    assert strategy[0].az == np.radians(200.0)
    assert strategy[0].alt == np.radians(36.0)
    
    source = gsm_point_src.SOURCES["Virtual_%s"%calib_src.src]
    assert np.allclose(strategy[-int(4*3600/2/params.strategy_step_size)].ra, source.ra) 
    assert np.allclose(strategy[-int(4*3600/2/params.strategy_step_size)].dec, source.dec)