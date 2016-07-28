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
    
