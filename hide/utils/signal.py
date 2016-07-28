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
Created on Nov 10, 2015

author: jakeret
'''

from __future__ import division

import numpy as np

def noisegen(beta=0, N=2**13):
    """
    Noise will be generated that has spectral densities that vary as powers of inverse frequency,
    more precisely, the power spectra P(f) is proportional to 1 / fbeta for beta >= 0. 
    When beta is 0 the noise is referred to white noise, when it is 2 it is referred to 
    as Brownian noise, and when it is 1 it normally referred to simply as 1/f noise 
    which occurs very often in processes found in nature. 
    
    The basic method involves creating frequency components which have a magnitude that is 
    generated from a Gaussian white process and scaled by the appropriate power of f. 
    The phase is uniformly distributed on 0, 2pi.
    
    from http://paulbourke.net/fractals/noise/
    
    :param beta:
    :param N: number of samples (can also be shape of array)
    
    :returns out: the sampled noise
    """
    assert np.all(beta>=0) and np.all(beta <= 3), "Beta must be between 0 and 3"
    
    if type(N) is tuple:
        nc, nn_ = N
        if nn_%2 == 1:
            nn = nn_ + 1
        else:
            nn = nn_
        real = np.zeros((nc, nn/2+1))
        imag = np.zeros((nc, nn/2+1))
        shape = (nc, nn/2)
        beta = np.atleast_1d(beta).reshape(-1,1)
    else:
        nn_ = N
        if nn_%2 == 1:
            nn = nn_ + 1
        else:
            nn = nn_
        real = np.zeros(nn/2+1)
        imag = np.zeros(nn/2+1)
        shape = nn/2
    
    freq = np.fft.helper.rfftfreq(nn)[1:]
    mag = np.power(freq, -beta / 2.0) * np.random.normal(0.0, 1.0, shape) # Note to self a number of years later, why "i+1"
    pha = np.random.uniform(0, 2 * np.pi, size = shape)
    real[...,1:] = mag * np.cos(pha)
    imag[...,1:] = mag * np.sin(pha)
    b = real + imag*1j

    out = np.fft.irfft(b, norm = "ortho")
    return out.real[...,:nn_]

# translated, not vectorized version
# def noisegen(N=2**13, beta=0, seed=42):
#     real = np.empty(N)
#     imag = np.empty(N)
# 
#     np.random.seed = seed
# 
#     real[0] = 0;
#     imag[0] = 0;
# 
#     for i in range(1,N/2):
#         mag = pow(i+1.0,-beta/2) * np.random.normal(0.0,1.0); # Note to self a number of years later, why "i+1"
#         pha = 2*np.pi * np.random.uniform()
#         real[i] = mag * np.cos(pha);
#         imag[i] = mag * np.sin(pha);
# 
#         real[N-i] =  real[i];
#         imag[N-i] = -imag[i];
# 
# 
#     imag[N/2] = 0;
#     b = real + imag*1j
# 
#     out = np.fft.ifft(b)
#     return out
