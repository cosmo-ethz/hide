# Copyright (C) 2013 ETH Zurich, Institute for Astronomy

'''
Created on Dec 8, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
import healpy as hp
from hide.beam import AxisSpec
from scipy import interpolate

def load_beam_profile(beam_spec, frequencies, params):
    """
    Creates a tophat beam profile for the given params definition 
    
    :param params: The params instance with the paramterization
    
    :returns profile: The top hat profile
    """

    beam_elevation = np.radians(params.beam_elevation)
    beam_azimut = np.radians(params.beam_azimut)
    beam_pixscale = np.radians(params.beam_pixscale)

    elevations = np.arange(-beam_elevation/2, beam_elevation/2, beam_pixscale)
    azimuts = np.arange(-beam_azimut/2, beam_azimut/2, beam_pixscale)
    frequencies = np.arange(params.beam_frequency_min, params.beam_frequency_max, params.beam_frequency_pixscale)
    
    def wd(i,j, sigma_i, sigma_j):
        return np.exp(-i**2/(2*sigma_i**2) - j**2/(2*sigma_j**2))
    
    cube = np.empty((len(elevations),
                     len(azimuts),
                     len(frequencies)),
                    dtype=np.float64)
    
    beam_norms = []
    for k, frequency in enumerate(frequencies):
        la = params.speed_of_light / (frequency * 10**6)
        fwhm = 1.0 * la / params.dish_diameter
        sigma = fwhm / (2. * np.sqrt(2. * np.log(2)))
        beam_norms.append(normalization(sigma, params.beam_nside))
        cube[:,:, k] = wd(*np.meshgrid(elevations, azimuts), sigma_i=sigma, sigma_j=sigma)
        
#         cube[:,:, k] = cube[:,:, k] / cube[:,:, k].sum() * params.beam_response
        
        
    beam_profile = cube
    axis = AxisSpec(elevations, azimuts, frequencies)
    
    beam_profiles = []
    for i, frequency in enumerate(np.arange(params.beam_frequency_min, params.beam_frequency_max, params.beam_frequency_pixscale)):
        response = beam_profile[:,:, i]
        f = interpolate.RectBivariateSpline(axis.elevation, axis.azimut, response)
        beam_profiles.append(spline(f.ev, params.beam_response))
    
    return beam_profiles, beam_norms
    
def normalization(sigma, nside):
    n = (4 * np.pi) * sigma * sigma
    pixarea = hp.nside2pixarea(nside, degrees=False)
    return pixarea/n
    
def spline(func, beam_response):
    def wrapped(x,y):
        Z = func(x,y)
        return Z
#         return Z / Z.sum() * beam_response
    return wrapped

        