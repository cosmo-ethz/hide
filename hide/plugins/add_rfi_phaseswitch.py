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
Created on Feb 17, 2016

author: seehars
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

from ivy.plugin.base_plugin import BasePlugin
from numpy import random
import importlib
from numpy import concatenate, ceil, pi
from scipy.signal.signaltools import fftconvolve
from datetime import timedelta

class Plugin(BasePlugin):
    """
    Adds RFI to the time ordered data (phase switch).
    
    """

    def __call__(self):
        params = self.ctx.params
        time = self.getTime()
        freq = self.ctx.frequencies
        if params.load_rfi_template:
            mod = importlib.import_module(self.ctx.params.instrument)
            rfifrac, rfiamplitude = mod.get_rfi_params(self.ctx.frequencies)
            params.rfifrac = rfifrac
            params.rfiamplitude = rfiamplitude
            
        try:
            rfiday = params.rfiday
        except AttributeError:
            rfiday = (0.0, 24.0)

        try:
            rfidamping = params.rfidamping
        except AttributeError:
            rfidamping = 1.0

        rfi = getRFI(params.white_noise_scale, params.rfiamplitude,
                     params.rfifrac, params.rfideltat,
                     params.rfideltaf, params.rfiexponent,
                     params.rfienhance, freq, time, rfiday, rfidamping)
        self.ctx.tod_vx += rfi
        self.ctx.tod_vx_rfi = rfi 

    def getTime(self):
        time = []
        for coord in self.ctx.strategy_coords:
            t = self.ctx.strategy_start + timedelta(seconds=coord.time)
            time.append(t.hour + t.minute / 60. + t.second / 3600.)
        return np.asarray(time)

    def __str__(self):
        return "Add RFI (phase switch)"

def getRFI(background, amplitude, fraction, deltat, deltaf, exponent, enhance,
           frequencies, time, rfiday, damping):
    """
    Get time-frequency plane of RFI.
     
    :param background: background level of data per channel
    :param amplitude: maximal amplitude of RFI per channel
    :param fraction: fraction of RFI dominated pixels per channel
    :param deltat: time scale of rfi decay (in units of pixels)
    :param deltaf: frequency scale of rfi decay (in units of pixels)
    :param exponent: exponent of rfi model (either 1 or 2)
    :param enhance: enhancement factor relative to fraction
    :param frequencies: frequencies of tod in MHz
    :param time: time of day in hours of tod
    :param rfiday: tuple of start and end of RFI day
    :param damping: damping factor for RFI fraction during the RFI night
    :returns RFI: time-frequency plane of RFI 
    """
    assert rfiday[1] >= rfiday[0], "Beginning of RFI day is after it ends."
    r = 1 - (rfiday[1] - rfiday[0]) / 24.
    nf = frequencies.shape[0]
    if (r == 0.0) | (r == 1.0):
        RFI = calcRFI(background, amplitude, fraction,
                      deltat, deltaf, exponent, enhance,
                      nf, time.shape[0])
    else:
        day_night_mask = getDayNightMask(rfiday, time)
        # Get fractions of day and night
        fday = np.minimum(1, fraction * (1 - damping * r)/(1 - r))
        fnight = (fraction - fday * (1 - r)) / r
        nday = day_night_mask.sum()
        nnight = time.shape[0] - nday
        RFI = np.zeros((nf, time.shape[0]))
        if nnight > 0:
            RFI[:,~day_night_mask] = calcRFI(background, amplitude, fnight,
                                             deltat, deltaf, exponent, enhance,
                                             nf, nnight)
        if nday > 0:
            RFI[:,day_night_mask] = calcRFI(background, amplitude, fday,
                                            deltat, deltaf, exponent, enhance,
                                            nf, nday)
    return RFI


def calcRFI(background, amplitude, fraction, deltat, deltaf, exponent, enhance,
           nf, nt):
    """
    Get time-frequency plane of RFI.
     
    :param background: background level of data per channel
    :param amplitude: maximal amplitude of RFI per channel
    :param fraction: fraction of RFI dominated pixels per channel
    :param deltat: time scale of rfi decay (in units of pixels)
    :param deltaf: frequency scale of rfi decay (in units of pixels)
    :param exponent: exponent of rfi model (either 1 or 2)
    :param enhance: enhancement factor relative to fraction
    :param nf: number of frequency channels
    :param nt: number of time steps
    :returns RFI: time-frequency plane of RFI 
    """
    lgb = np.log(background)
    lgA = np.log(amplitude)
    d = lgA - lgb
    # choose size of kernel such that the rfi is roughly an order of magnitude
    # below the background even for the strongest RFI
    Nk = int(ceil(np.amax(d))) + 3
    t = np.arange(nt)
    if exponent == 1:
        n = d * d * (2. * deltaf * deltat / 3.0)
    elif exponent == 2:
        n = d * (deltaf * deltat * pi *.5)
    else:
        raise ValueError('Exponent must be 1 or 2, not %d'%exponent)
    neff = fraction * enhance * nt / n
    N = np.minimum(random.poisson(neff, nf), nt)
    RFI = np.zeros((nf,nt))
    dt = int(ceil(.5 * deltat))
    # the negative indices really are a hack right now
    neginds = []
    for i in range(nf):
#         trfi = choice(t, N[i], replace = False)
        trfi = random.permutation(t)[:N[i]]
#         trfi = randint(0,nt,N[i])
        r = random.rand(N[i])
        tA = np.exp(r * d[i] + lgb[i])
        r = np.where(random.rand(N[i]) > .5, 1, -1)
        sinds = []
        for j in range(dt):
            fac = (-1)**j * (j + 1) * dt
            sinds.append(((trfi + fac * r) % nt))
        neginds.append(concatenate(sinds))
        RFI[i,trfi] = tA
    k = kernel(deltaf, deltat, nf, nt, Nk, exponent)
    RFI = fftconvolve(RFI, k, mode = 'same')
#     neginds = np.unique(concatenate(neginds))
#     RFI[:,neginds] *= -1
    df = int(ceil(deltaf))
    for i, idxs in enumerate(neginds):
        mif = np.maximum(0, i-df)
        maf = np.minimum(nf, i+df)
        RFI[mif:maf,idxs] *= -1
    return RFI

def getDayNightMask(rfiday, time):
    return (rfiday[0] < time) & (time < rfiday[1])

def logmodel(x, dx, exponent):
    """
    Model for the log of the RFI profile:
     * -abs(x)/dx for exponent 1
     * -(x/dx)^2 for exponent 2

    :param x: grid on which to evaluate the profile
    :param dx: width of exponential
    :param exponent: exponent of (x/dx), either 1 or 2
    :returns logmodel: log of RFI profile
    """
    if exponent == 1:
        return -np.absolute(x)/dx
    elif exponent == 2:
        return -(x * x) / (dx * dx)
    else:
        raise ValueError('Exponent must be 1 or 2, not %d'%exponent)
    
def kernel(deltaf, deltat, nf, nt, N, exponent):
    """
    Convolution kernel for FFT convolution
    
    :param deltaf: spread of RFI model in frequency
    :param deltat: spread of RFI model in time
    :param nf: number of frequencies
    :param nt: number of time steps
    :param N: size of kernel relative to deltaf, deltat
    :param exponent: exponent of RFI model (see logmodel)
    :returns kernel: convolution kernel
    """
    fmax, tmax = np.minimum([N * deltaf, N * deltat], [(nf-1)/2,(nt-1)/2])
    f = np.arange(2*fmax+1) - fmax
    t = np.arange(2*tmax+1) - tmax
    return np.outer(np.exp(logmodel(f, deltaf, exponent)), np.exp(logmodel(t, deltat, exponent)))