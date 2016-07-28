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
import hide.utils.quaternion as qu 
from hide.utils import ARCCOS_ATOL

def test_inv():
    q1 = np.array([[1,1,1,1]])
    q1i = qu.inv(q1)
    assert np.all(q1 == qu.inv(q1i))
    
def test_mult():
#     from https://www.youtube.com/watch?v=Ne3RNhEVSIE&list=PLW3Zl3wyJwWOpdhYedlD-yCB7WQoHf-My&index=33
    q1 = qu.vecquad(0,1,0,np.radians(90))
    q2 = qu.vecquad(1,0,0,np.radians(45))
    q3 = qu.mult(q2, q1)
    
    assert np.allclose(q1, [[ 0.,0.7071, 0., 0.7071]])
    assert np.allclose(q2, [[ 0.382683,  0.,  0.,  0.92388 ]])
    assert np.allclose(q3, [[ 0.270598,  0.653281,  0.270598,  0.653281]])
    
def test_rotate_vec():
    q1 = qu.vecquad(0,1,0,np.radians(90))
    q2 = qu.vecquad(1,0,0,np.radians(45))
    q3 = qu.mult(q2, q1)
    v1 = np.atleast_2d([1,0,0])
    
    vr1s = qu.rotate_vec_slow(q1, v1)
    vr2s = qu.rotate_vec_slow(q2, vr1s)
    vr3s = qu.rotate_vec_slow(q3, v1)
    
    assert np.allclose(vr1s, [[0,0,-1]])
    assert np.allclose(vr2s, [[0, np.sqrt(2)/2, -np.sqrt(2)/2]])
    assert np.allclose(vr3s, vr2s)
    
    vr1 = qu.rotate_vec(q1, v1)
    vr2 = qu.rotate_vec(q2, vr1)
    vr3 = qu.rotate_vec(q3, v1)
    
    assert np.allclose(vr1, vr1s)
    assert np.allclose(vr2, vr2s)
    assert np.allclose(vr3, vr3s)

    vr1o = qu.rotate_vec_opt(q1, v1)
    vr2o = qu.rotate_vec_opt(q2, vr1o)
    vr3o = qu.rotate_vec_opt(q3, v1)
    
    assert np.allclose(vr1o, vr1s)
    assert np.allclose(vr2o, vr2s)
    assert np.allclose(vr3o, vr3s)

# def test_cross():
#     u = np.array([[1.3, 3.4, 4.5], [2.3, 4.7, 6.8]])
#     v = np.array([[2.3, 4.4, 7.5], [0.3, 1.7, 3.8]])
# 
#     assert np.all(np.cross(u, v) == qu._cross(u, v))
# 
#     u = np.array([[0., np.sqrt(2)/2, 0.]])
#     v = np.array([[1., 0., 0.]])
#     assert np.all(np.cross(u, v) == qu._cross(u, v))


def test_rotator():
    size = 10
    theta = np.random.uniform(0, np.pi, size)
    phi = np.random.uniform(0, 2*np.pi, size)
    
    q1 = qu.vecquad(0, 1, 0, np.random.uniform(0, 2*np.pi))
    q2 = qu.vecquad(0, 0, 1, np.random.uniform(0, 2*np.pi))
    q = qu.mult(q2, q1)
    rotator = qu.Rotator(q)
    rtheta, rphi = rotator(*rotator(theta, phi), inverse=True)
    rtheta = rtheta%np.pi
    rphi = rphi%(2*np.pi)
    
    assert np.allclose(theta, rtheta)
    assert np.allclose(phi, rphi)
    
    
    