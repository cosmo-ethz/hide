# Copyright (C) 2013 ETH Zurich, Institute for Astronomy

'''
Created on Dec 8, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
import healpy as hp
from hide.beam import AxisSpec

def load_beam_profile(beam_spec, frequencies, params):
    """
    Creates a tophat beam profile for the given params definition 
    
    :param params: The params instance with the paramterization
    
    :returns profile: The top hat profile
    """
#     beam_elevation = np.radians(params.beam_elevation)
#     beam_azimut = np.radians(params.beam_azimut)
#     beam_pixscale = np.radians(params.beam_pixscale)
    
#     elevations = np.arange(-beam_elevation/2, beam_elevation/2, beam_pixscale)
#     azimuts = np.arange(-beam_azimut/2, beam_azimut/2, beam_pixscale)
#     frequencies = np.arange(params.beam_frequency_min, params.beam_frequency_max, params.beam_frequency_pixscale)

    
#     cube = np.zeros((len(elevations),
#                      len(azimuts),
#                      len(frequencies)),
#                     dtype=np.float64)

    center_x, center_y = 0,0
    r = np.amin([beam_spec.dec[-1], beam_spec.ra[-1]])
    beam_profiles = [_top_hat(r, center_x, center_y, params.beam_response) for _ in frequencies]
    beam_norms = [normalization(r, params.beam_nside) for _ in frequencies]
    return beam_profiles, beam_norms
#     x = np.arange(0, cube.shape[0])
#     y = np.arange(0, cube.shape[1]).reshape(-1, 1)
#     
#     dist = np.sqrt((x-center_x)**2 + (y-center_y)**2)
#     
#     mask = dist < r
#     
#     cube[mask] = 1
#     
#     cube = cube / cube.sum() * params.beam_response * len(frequencies)
# 
#     x = np.linspace(-1, 1 + beam_pixscale / 2, len(x)) * beam_elevation / 2
#     y = np.linspace(-1, 1 + beam_pixscale / 2, len(x)).reshape(-1, 1) * beam_azimut / 2
# 
#     return cube, AxisSpec(elevations, azimuts, frequencies)

def normalization(r, nside):
    n = np.pi * r * r
    pixarea = hp.nside2pixarea(nside, degrees=False)
    return pixarea/n

def _top_hat(r, center_x, center_y, beam_response):
    def wrapped(x,y):
        dist = np.sqrt((x-center_x)**2 + (y-center_y)**2)
        Z = np.where(dist<r, 1, 0)
        return Z
#         return Z / Z.sum() * beam_response
    return wrapped
