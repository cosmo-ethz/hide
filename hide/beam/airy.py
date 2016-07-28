# HIDE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# HIDE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with HIDE.  If not, see <http://www.gnu.org/licenses/>.


'''
Created on Apr 25, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from pkg_resources import resource_filename

import numpy as np
import healpy as hp
import scipy.special as sp

import hide
import hope

PROFILE_PATH = "data/sun_gain_template.dat"

def load_beam_profile(beam_spec, frequencies, params):
    """
    Creates a 2d airy beam profile using the given gain template
    
    :param params: The params instance with the paramterization
    
    :returns profile: A list of callable beam profiles
    """

    path = resource_filename(hide.__name__, PROFILE_PATH)
    gain_sun = np.genfromtxt(path, skip_header=True)
    sun_freq = gain_sun[:,0]
    sun_Ae = np.radians(gain_sun[:,2])

    sigmas = np.interp(frequencies, sun_freq, sun_Ae)
    fwhms = sigma2fwhm(sigmas)
    
    beam_profiles = [airy_wrapper(fwhm) for fwhm in fwhms]
    beam_norms = [normalization(fwhm, params.beam_nside) for fwhm in fwhms]
    return beam_profiles, beam_norms

def sigma2fwhm(sigma):
    return 2 * np.sqrt(2 * np.log(2)) * sigma / 1.028

def normalization(fwhm, nside):
    r = fwhm/np.pi
    n = (4 * np.pi) * r * r
    pixarea = hp.nside2pixarea(nside, degrees=False)
    return pixarea/n

def airy_wrapper(fwhm):
    def wrapped(x, y):
        r = np.sqrt(x**2 + y**2)
        t = np.pi * r / (fwhm)
        Z = (2 * sp.j1(t) / t)**2
        return Z
    return wrapped

_TABLERANGE = 2**11
_BESSEL_J1_TABLE = sp.j1(np.linspace(0.0, 6.0, _TABLERANGE+1, dtype=np.float64))
_C = np.float64(_TABLERANGE / 6.0)

@hope.jit
def _bessel_j1_hope(x, xs0, y, table, C):
    for i in range(xs0):
        xi = np.float64(x[i] * C)
        xl = np.uint32(xi)
        b = xi-np.float64(xl)
        y[i] = (1-b)*table[xl] + b*table[xl+1]


def bessel_j1(x):
    y = np.empty((len(x)))
    _bessel_j1_hope(x, len(x), y, _BESSEL_J1_TABLE, _C)
    return y

