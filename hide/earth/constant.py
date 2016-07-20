# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Nov 25, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
import healpy as hp

def load_signal(ctx):
    """
    Returns a constant signal
    
    :param ctx: context object containing params
    
    :returns earth_signal: healpy map with the signal
    """
    nside = ctx.params.beam_nside
    earth_signal = ctx.params.earth_signal_flux * np.ones(hp.nside2npix(nside), np.float32)
    
    return earth_signal