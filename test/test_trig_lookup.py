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
from hide.utils import sin_cos
import pytest
from hide.utils import arccos

def test_sin_cos_lookup():
    x = np.linspace(-4*np.pi, 4*np.pi, 1000)
    sins, coss = np.sin(x), np.cos(x)
    sins2, coss2 = sin_cos(x)
    assert np.allclose(sins, sins2)
    assert np.allclose(coss, coss2)
    
def test_sin_cos_scalar():
    with pytest.raises(TypeError):
        sin_cos(0)

def test_arccos_lookup():
    x = np.cos(np.linspace(-4.*np.pi, 4.*np.pi, 1000))
    arccoss = np.arccos(x)
    arccoss2 = arccos(x)
    assert np.allclose(arccoss, arccoss2, atol=6.7e-5)
     
def test_arccos_scalar():
    with pytest.raises(TypeError):
        arccos(0)
