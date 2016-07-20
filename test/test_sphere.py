# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Feb 23, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from hide.utils import sphere
from hide.utils import ARCCOS_ATOL

def test_dir2vec():
    size = 10
    theta = np.random.uniform(0, np.pi, size)
    phi = np.random.uniform(0, 2*np.pi, size)
    
    vec = sphere.dir2vec(theta, phi)
    theta2, phi2 = sphere.vec2dir(vec)
    
    assert np.allclose(theta, theta2, atol=ARCCOS_ATOL)
    assert np.allclose(phi, phi2%(2*np.pi))
    
