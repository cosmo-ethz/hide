# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Jan 15, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from datetime import timedelta
import numpy as np

from hide.strategy import CoordSpec
from hide.utils import sidereal


def load_strategy(ctx):
    """
    Creates a scanning strategy that uses drift mode i.e. the 
    telescope stares at the same position for 24 hours and then changes the altiude by a certain angle
    
    :param ctx: The ctx instance with the paramterization
    
    :returns strategy: A list of CoordSpec with the scanning strategy
    """
    
    start = ctx.strategy_start
    end   = ctx.strategy_end
    
    diff = end-start

    lat_lon = sidereal.LatLon(np.radians(ctx.params.telescope_latitude), 
                              np.radians(ctx.params.telescope_longitude))
    
    alt_delta = np.radians(ctx.params.alt_delta)
    az_pos = np.radians(ctx.params.azimuth_pointing)
    alt_pos = np.radians(ctx.params.altitude_start_pos)
    alt_max = np.radians(ctx.params.altitude_max_pos)
    
    strategy = []
    
    sec_per_day = 24*60*60
    duration = int(diff.total_seconds())
    for sec in range(0, duration, ctx.params.strategy_step_size):
        gst = sidereal.SiderealTime.fromDatetime(start + timedelta(seconds=sec))
        radec = sidereal.AltAz(alt_pos, az_pos).raDec(gst.lst(lat_lon.lon), lat_lon)
        
        strategy.append(CoordSpec(sec, alt_pos, az_pos, radec.ra, radec.dec))
        if sec % sec_per_day == 0 and sec != 0:
            alt_pos += alt_delta
            
        if alt_pos > alt_max:
            alt_pos = np.radians(ctx.params.altitude_start_pos)
                
    return strategy
