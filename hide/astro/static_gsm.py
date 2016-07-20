# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Jan 7, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import healpy as hp 
from pkg_resources import resource_filename
import hide

FILE_PATH = "data/gsm_map.fits"

GSM_NSIDE = 2**9

def load_signal(ctx):
    """
    Returns the same global sky model (GSM) map independent of the frequency.
    Rescales the map if neccessary (if param.beam_nside != 512)
    
    :param params: The ctx instance with the paramterization
    :returns signal: The astro signal
    """
    
    path = resource_filename(hide.__name__, FILE_PATH)
    gsm_map = hp.read_map(path, verbose=False)
    if ctx.params.beam_nside != GSM_NSIDE:
        gsm_map = hp.ud_grade(gsm_map, nside_out=ctx.params.beam_nside)
        
    return gsm_map