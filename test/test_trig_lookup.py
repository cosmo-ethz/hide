# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

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
