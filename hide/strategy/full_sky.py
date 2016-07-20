# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

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