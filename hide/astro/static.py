# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 8, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
import healpy as hp

def load_signal(ctx):
    """
    Creates a sphere with a static flux as signal for the given ctx ( and params)
         
    :param params: The ctx instance with the paramterization
    :returns signal: A static signal
    """
    npix = hp.nside2npix(ctx.params.beam_nside)
    cosmic_sphere = ctx.params.astro_flux * np.ones(npix)
    
    return cosmic_sphere
