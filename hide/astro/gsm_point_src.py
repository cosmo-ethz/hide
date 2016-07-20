# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Apr 22, 2016

In large parts a copy of astro_calibration_sources in seek by cchang.

Models taken from: Baars 1997, Hafez 2008, Benz 2009
All numbers divided by 2 to account for polarization.

Coordinates from wikipedia

author: seehars, jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from collections import namedtuple

import numpy as np
import healpy as hp

from hide.astro import gsm
from hide.utils import sphere

AstroSource = namedtuple("AstroSource", ["model", "ra", "dec"])

DEFAULT_OBJECTS = ["CasA", "CygA", "SagA", "TauA", "VirA"]

h = 6.626e-34
k = 1.38e-23
c = 3.0e8
pi2 = 2 * np.pi

def load_signal(ctx):
    """
    Returns an interpolated global sky model (GSM) map dependent on the frequency and adds radio point srcs.
    
    :param params: The ctx instance with the paramterization
    :returns signal: The astro signal
    """
    astro_signal = gsm.load_signal(ctx)
    add_point_sources(ctx.frequency, 
                      ctx.params.beam_nside,
                      astro_signal, 
                      ctx.params.astro_point_srcs)
    
    return astro_signal
    
def add_point_sources(freq, nside, astro_signal, objects=None):
    if objects is None: objects = DEFAULT_OBJECTS
    
    lam = c/(freq*1e6)
    pixarea = hp.nside2pixarea(nside, degrees=False)
    ae = lam * lam / pixarea
    for obj in objects:
        source = SOURCES[obj]
        theta = sphere.dec2theta(source.dec)
        phi = sphere.ra2phi(source.ra)
        idx = hp.ang2pix(nside, theta, phi)
        
        jansky = source.model(freq)
        
        T = convertunits(jansky, ae)
        # in principle one could already correct for the effect of the 
        # finite pixel size at this point
        astro_signal[idx] = T
   
def convertunits(s, ae):
    return ae * s / 2. / k * 1e-26
    
# Astro source models
def barrs77_power_law(freq, a, b, c):
    return 10**(a + b * np.log10(freq) + c * np.log10(freq)**2)

def cas_a_model(freq):
    F = (0.68 - 0.15 * np.log10(freq / 1.0e3) * (2015 - 1970)) * 0.01
    return (1.0 + F) * barrs77_power_law(freq, 5.88, -0.792, 0.0)

def cyg_a_model(freq):
    return barrs77_power_law(freq, 4.695, 0.085, -0.178)

def sag_a_model(freq):
    return barrs77_power_law(freq, 5.88, -0.792, 0.0)

def tau_a_model(freq):
    return barrs77_power_law(freq, 3.915, -0.299, 0.0)

def vir_a_model(freq):
    return barrs77_power_law(freq, 5.023, -0.856, 0.0)


SOURCES = dict(CasA = AstroSource(cas_a_model, 
                                  ra = (23 + 23/60. + 26/3600.)/24. * pi2, 
                                  dec = (58 + 48/60.)/360. * pi2),
               CygA = AstroSource(cyg_a_model, 
                                  ra = (19 + 59/60. + 28.3566/3600.)/24. * pi2, 
                                  dec = (40 + 44/60. + 2.096/3600.)/360. * pi2),
               SagA = AstroSource(sag_a_model, 
                                  ra = (17 + 45/60. + 40.0409/3600.)/24. * pi2, 
                                  dec = (-29.0 + 28.118/3600.)/360. * pi2),
               TauA = AstroSource(tau_a_model, 
                                  ra = (5 + 34/60. + 31.94/3600.)/24. * pi2, 
                                  dec = (22 + 52.2/3600.)/360. * pi2),
               VirA = AstroSource(vir_a_model, 
                                  ra = (12 + 30/60. + 49.42338/3600.)/24. * pi2, 
                                  dec = (12 + 23/60. + 28.0439/3600.)/360. * pi2),
               Virtual_CasA = AstroSource(cas_a_model, 
                                  ra = 0.5,  
                                  dec = 1.0262536001726656),
               Virtual_CygA = AstroSource(cyg_a_model, 
                                  ra = 1.5, 
                                  dec = 0.7109409436737796),
               Virtual_SagA = AstroSource(sag_a_model, 
                                  ra = 2.1, 
                                  dec = -0.5060091631675012),
               Virtual_TauA = AstroSource(tau_a_model, 
                                  ra = 5.3, 
                                  dec = 0.3842255081802917),
               Virtual_VirA = AstroSource(vir_a_model, 
                                  ra = 2.8, 
                                  dec = 0.2162658997025478),
               )
