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
Created on Jan 7, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

from hide.strategy import CoordSpec
from hide.utils import sidereal
from datetime import timedelta

EPS = 1e-5

def load_strategy(ctx):
    """
    Creates a crosshair in RA/DEC scanning strategy
    
    :param ctx: The ctx instance with the parameterization
    
    :returns strategy: A crosshair scanning strategy
    """
    
    start = ctx.strategy_start
    end   = ctx.strategy_end
    
    lat = np.radians(ctx.params.telescope_latitude)
    lon = np.radians(ctx.params.telescope_longitude)
    
    diff = int((end-start).total_seconds())
    step = ctx.params.strategy_step_size
    duration = int(diff // step)

#     ra_coords = [CoordSpec(durration//2 + t, 0, 0, ra, 0) for t, ra in enumerate(np.linspace(-np.pi, np.pi, durration//2))]
    
    strategy = []
    ra = 0
    for sec, dec in enumerate(np.linspace(-np.pi/2+EPS, np.pi/2-EPS, duration//2)):
        dt = sec*step
        date = start + timedelta(seconds=dt)
        radec = sidereal.RADec(ra, dec)
        h = radec.hourAngle(date, lon)
        altaz = radec.altAz(h, lat)
        strategy.append(CoordSpec(dt, altaz.alt + np.pi, altaz.az, ra, dec))

    dec_end = sec*step
    dec = 0
    for sec, ra in enumerate(np.linspace(-np.pi+EPS, np.pi, duration//2)):
        dt = dec_end+sec*step
        date = start + timedelta(seconds=dt)
        radec = sidereal.RADec(ra, dec)
        h = radec.hourAngle(date, lon)
        altaz = radec.altAz(h, lat)
        strategy.append(CoordSpec(dt, altaz.alt + np.pi, altaz.az, ra, dec))
    
    return strategy