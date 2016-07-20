# Copyright (C) 2016 ETH Zurich, Institute for Astronomy

'''
Created on Mar 24, 2016

author: seehars
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import importlib
from datetime import datetime, timedelta
from collections import defaultdict

import numpy as np

from hide.strategy import CoordSpec
from hide.utils import sphere

DATEFORMAT = '%Y-%m-%d%H:%M'
DAYFORMAT = '%Y-%m-%d'

class ScheduleEntry(object):
    
    def __init__(self, date, az, el, mode):
        self.date = date
        self.az = az
        self.el = el
        
        if mode is None or mode == "Survey":
            self.mode = "Survey"
        else:
            self.mode, src = mode.split(":")
            self.src = src.strip()
    
    def day(self):
        return self.date.strftime(DAYFORMAT)
    
    def is_survey(self):
        return "Survey" == self.mode
    
    def delta(self, other):
        return int((other.date - self.date).total_seconds())
        

def parse_schedule(path, strategy_start):
    """
    Parses a scheduler file
    :param path: the path to the scheduler file
    :param strategy_start: start date of the strategy
    
    :returns schedule_entries: list of `ScheduleEntry`
    """
    with open(path, "r") as fh:
        schedule_entries = [_parse_schedule_entry(line, strategy_start) for line in fh]
    return schedule_entries

def _parse_schedule_entry(line, strategy_start):
    day, time, az, el, mode = line.strip('\n').strip('\r').split(", ")
    date = datetime.strptime(day+time, DATEFORMAT)
    return ScheduleEntry(max([date, strategy_start]), 
                         np.radians(float(az)), 
                         np.radians(float(el)), 
                         mode)

def process_schedule(schedule, step_size, strategy_start, strategy_end, obs):
    """
    Processes a list of schedule entries
    :param schedule: the list of schedule entries 
    :param step_size: the step size to use
    :param strategy_start: start date of the strategy
    :param strategy_end: end date of the strategy
    :param obs: telescope position
    
    :returns strategy, calibration_days: a list of `CoordSpec` and a dict for the calibration days
    """
    strategy = []
    calibration_days = defaultdict(list)
    schedule_end = ScheduleEntry(strategy_end, None, None, None)
    for current_entry, next_entry in zip(schedule, schedule[1:]+[schedule_end]):
        if current_entry.date >= strategy_end:
            break
        
        time_delta = current_entry.delta(next_entry)
        for sec in range(0, time_delta, step_size):
            strategy.append(_create_cood_spec(current_entry, sec, strategy_start, obs))
            
        if not current_entry.is_survey():
            calibration_days[current_entry.day()].append(current_entry)
            
    return strategy, calibration_days

def _create_cood_spec(schedule_entry, sec, strategy_start, obs):
    time = schedule_entry.date + timedelta(seconds=sec)
    ra, dec = sphere.altaz_to_ra_dec(time, schedule_entry.az, schedule_entry.el, obs)
    total = (time - strategy_start).total_seconds()
    return CoordSpec(total, schedule_entry.el, schedule_entry.az, ra, dec)


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

    strategy, calibration_days = process_schedule(parse_schedule(path, ctx.strategy_start), 
                                                      ctx.params.strategy_step_size, 
                                                      ctx.strategy_start, 
                                                      ctx.strategy_end, 
                                                      obs = sphere.get_observer(ctx))
    ctx.calibration = calibration_days
    
    return strategy

