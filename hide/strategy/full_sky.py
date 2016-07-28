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
Created on Jan 15, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
import healpy as hp
import itertools


from hide.strategy import CoordSpec
from hide.utils import sidereal
from hide.utils import sphere
from datetime import timedelta


def load_strategy(ctx):
    """
    Creates a scanning strategy that covers the full sky
    
    :param ctx: The ctx instance with the paramterization
    
    :returns strategy: A list of CoordSpec with the scanning strategy for the full sky
    """
    start = ctx.strategy_start
    
    lat = np.radians(ctx.params.telescope_latitude)
    lon = np.radians(ctx.params.telescope_longitude)

    beam_nside = ctx.params.beam_nside
    thetas,phis = hp.pix2ang(beam_nside, np.arange(hp.nside2npix(beam_nside)))
    decs = sphere.theta2dec(thetas)
    ras = sphere.phi2ra(phis)
    
    strategy = []
    for sec, (ra,dec) in enumerate(itertools.izip(ras, decs)):
        date = start + timedelta(seconds=sec)
        radec = sidereal.RADec(ra, dec)
        h = radec.hourAngle(date, lon)
        altaz = radec.altAz(h, lat)
        strategy.append(CoordSpec(sec, altaz.alt + np.pi, altaz.az, ra, dec))

    return strategy