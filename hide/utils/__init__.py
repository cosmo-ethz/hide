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
Created on Feb 20, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from datetime import datetime

import hope
from hide import DATE_FORMAT


ARCCOS_ATOL=6.7e-5

_TABLERANGE = 2**11
_SINTABLE = np.sin(np.linspace(0, 2. * np.pi, _TABLERANGE+1, dtype=np.float64))
_COSTABLE = np.cos(np.linspace(0, 2. * np.pi, _TABLERANGE+1, dtype=np.float64))

@hope.jit
def _sin_cos_hope(x, xs0, y, tablerange, sinTable, cosTable):
    twopi = (2*np.pi)
    for i in range(xs0):
        xi = np.uint32(x[i] * 2**32/twopi)
        xl = np.uint32(xi >> (32-11))
        b = np.float64(xi & np.uint32((1 << (32 - 11)) - 1)) / np.float64(1 << (32 - 11))
        y[i, 0] = (1-b)*sinTable[xl] + b*sinTable[xl+1]
        y[i, 1] = (1-b)*cosTable[xl] + b*cosTable[xl+1]

def sin_cos(x):
    y = np.empty((len(x), 2))
    _sin_cos_hope(x, len(x), y, int(_TABLERANGE), _SINTABLE, _COSTABLE)
    return y[:, 0], y[:, 1]

@hope.jit
def _arccos_hope(xs, xs0, y):
    for i in range(xs0):
        x = xs[i]
        negate = np.float64(x<0)
        x=np.fabs(x)
        ret = -0.0187293
        ret = ret * x
        ret = ret + 0.0742610
        ret = ret * x
        ret = ret - 0.2121144
        ret = ret * x
        ret = ret + 1.5707288
        ret = ret * np.sqrt(1.0-x)
        ret = ret - 2. * negate * ret
        y[i] = negate * 3.14159265358979 + ret
        
def arccos(x):
    y = np.empty_like(x)
    _arccos_hope(x,len(x), y)
    return y

def parse_datetime(s):
    return datetime.strptime(s, DATE_FORMAT)

