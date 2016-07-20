# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on May 4, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import importlib
from datetime import timedelta

from hide.strategy import scheduler
from hide.astro import gsm_point_src
from hide.utils import sphere

def replace_calibrations(schedule, obs):
    for entry in schedule:
        if not entry.is_survey():
            src_name = "Virtual_%s"%entry.src
            try:
                source = gsm_point_src.SOURCES[src_name]

                obs_time = 2 * 60 *60
                date = entry.date + timedelta(seconds=obs_time / 2)
                alt, az = sphere.radec_to_altaz(date, source.ra, source.dec, obs)
                entry.az = az
                entry.el = alt
            except KeyError:
                pass
            

def load_strategy(ctx):
    """
    Creates a scanning strategy from a scheduler file.
    
    :param ctx: The ctx instance with the path to the scheduler file
    
    :returns strategy: A list of CoordSpec with the scanning strategy
    """
    if ctx.params.scheduler_file == "default":
        mod = importlib.import_module(ctx.params.instrument)
        path = mod.get_schedule()
    else:
        path = ctx.params.scheduler_file

    obs = sphere.get_observer(ctx)
    
    schedule_entries = scheduler.parse_schedule(path, ctx.strategy_start)
    replace_calibrations(schedule_entries, obs)
    strategy, calibration_days = scheduler.process_schedule(schedule_entries,
                                                            ctx.params.strategy_step_size,
                                                            ctx.strategy_start,
                                                            ctx.strategy_end,
                                                            obs)
    ctx.calibration = calibration_days
    
    return strategy

