# Copyright (C) 2013 ETH Zurich, Institute for Astronomy

'''
Created on Dec 8, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
import healpy as hp
from hope import jit

def load_beam_profile(beam_spec, frequencies, params):
    """
    Creates a 2d gaussian beam profile for the given params definition 
    
    :param params: The params instance with the paramterization
    
    :returns profile: A list of callable beam profiles
    """

    beam_profiles = []
    beam_norms = []
    for k, frequency in enumerate(frequencies):
        la = params.speed_of_light / (frequency * 10**6)
        fwhm = 1.0 * la / params.dish_diameter
        sigma = fwhm / (2. * np.sqrt(2. * np.log(2)))
        beam_norms.append(normalization(sigma, params.beam_nside))
        beam_profiles.append(gauss_wrapper(sigma, params.beam_response))
    return beam_profiles, beam_norms

# def _2d_gauss(sigma, beam_response):
#     i2sigma2 = 1. / (2*sigma**2)
#     def wrapped(i,j):
# #         Z =  np.exp(-i**2/(2*sigma**2) - j**2/(2*sigma**2))
#         Z =  np.exp(i2sigma2 * (-i**2 - j**2))
#         return Z / Z.sum() * beam_response
#     return wrapped


# cumbersome call to avoid mem leak in hope
def gauss_wrapper(sigma, beam_response):
    i2sigma2 = 1. / (2*sigma**2)
    def wrapped(i,j):
        Z = np.empty_like(i)
        hope_gauss(i2sigma2, beam_response, i, j, Z)
        return Z
    return wrapped

def normalization(sigma, nside):
    n = (4 * np.pi) * sigma * sigma
    pixarea = hp.nside2pixarea(nside, degrees=False)
    return pixarea/n

@jit
def hope_gauss(i2sigma2, beam_response, i, j, Z):
    Z[:] =  np.exp(i2sigma2 * (-i**2 - j**2))
    #Z /= np.sum(Z) * beam_response
