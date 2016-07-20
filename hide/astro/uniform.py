# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Jan 7, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
import healpy as hp

def load_signal(ctx):
    """
    Creates a sphere with a uniform flux as signal for the given ctx ( and params) 
    
    :param params: The ctx instance with the paramterization
    :returns signal: A static signal
    """
    npix = hp.nside2npix(ctx.params.beam_nside)
    cosmic_sphere = np.arange(npix)
    
    return cosmic_sphere