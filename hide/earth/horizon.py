# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 8, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
import healpy as hp

from hide.utils import sphere

def load_signal(ctx):
    """
    Models effect of the horizon
    
    :param ctx: context object containing params
    
    :returns earth_signal: healpy map with the signal
    """
    nside = ctx.params.beam_nside
    idx = np.arange(hp.nside2npix(nside))
    thetas, _ = hp.pix2ang(nside, idx)
    dec = sphere.theta2dec(thetas)
    
    min_mask = (dec<ctx.params.vmin) 
    max_mask = (dec>ctx.params.vmax)
    mask = min_mask | max_mask
    earth_signal = np.zeros(hp.nside2npix(nside))
    
    fit = np.poly1d(ctx.params.fit_coeffs)
    earth_signal[~mask] = fit(dec[~mask])
    earth_signal[min_mask] = fit(ctx.params.vmin)
    earth_signal[max_mask] = fit(ctx.params.vmax)
    earth_signal[:] = ctx.params.log_base**earth_signal
        
    return earth_signal
