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

# coding: utf-8
from __future__ import division

import numpy as np
from numpy import sin, cos, arccos
from hide.utils import sin_cos
from hide.utils import sphere

def vecquad(x,y,z,w):
    """create a quaternion from a euler vector with angle"""
    q = np.empty((1, 4))
    sin_w, cos_w = sin_cos(np.atleast_1d(w/2))
    q[:, 0] = x
    q[:, 1] = y
    q[:, 2] = z
    q[:, :3] = q[:, :3] * sin_w
    q[:, 3] = cos_w
    return q
    

# def quad(theta, phi, a=0):
#     """create a imaginary quaternions from spherical coords"""
#     sin_t, cos_t = sin_cos(theta)
#     sin_p, cos_p = sin_cos(phi)
#     vec = np.ones((len(theta), 4))
#     vec[:,0] = sin_t * cos_p
#     vec[:,1] = sin_t * sin_p
#     vec[:,2] = cos_t
#     vec[:,3] *= a
#     return vec

def inv(q):
    """Inverse of quaternion array q"""
    return q * np.array([-1,-1,-1,1])

def norm(q):
    """Normalize quaternion array q to unit quaternions"""
    return q/np.sqrt(np.sum(np.square(q),axis=1))[:,np.newaxis]

def mult(p, q):
    '''Multiply arrays of quaternions, ndarray objects with 4 columns defined as x y z w
    see:
    http://en.wikipedia.org/wiki/Quaternions#Quaternions_and_the_geometry_of_R3
    '''
    if p.ndim == 1 and q.ndim > 1:
        p = np.tile(p,(q.shape[0],1))
    if q.ndim == 1 and p.ndim > 1:
        q = np.tile(q,(p.shape[0],1))
    if q.ndim == 1 and p.ndim == 1:
        p = p.reshape((1,4))
        q = q.reshape((1,4))

    ps = p[:,3]
    qs = q[:,3]
    pv = p[:,:3]
    qv = q[:,:3]

    if p.size>q.size:
        pq = np.empty_like(p)
    else:
        pq = np.empty_like(q)
    
    pq[:,3] =  ps * qs - np.sum(pv*qv, axis=1)
    pq[:,:3] = ps[:,np.newaxis] * qv + pv * qs[:,np.newaxis] + np.cross(pv , qv)

    #opposite sign due to different convention on the basis vectors
    #pq = -1 * pq
    return pq

def rotate_vec_slow(q, v):
    """Rotate or array of vectors v by quaternion q"""
    qv = np.zeros((v.shape[0], 4))
    qv[:, :3] = v
    return mult(mult(q, qv), inv(q))[:, :3]
#     return mult(q, mult(qv, inv(q)))[:, :3]


# def _cross(u, v):
#     s2 = np.empty(v.shape)
#     s2[:, 0] = u[:, 1] * v[:, 2] - u[:, 2] * v[:, 1]
#     s2[:, 1] = u[:, 2] * v[:, 0] - u[:, 0] * v[:, 2]
#     s2[:, 2] = u[:, 0] * v[:, 1] - u[:, 1] * v[:, 0]
#     return s2

def rotate_vec(q, v):
    """Rotate or array of vectors v by quaternion q"""
    Wq = q[:,3]
    Vq = q[:,:3]
    C = Wq * v + np.cross(Vq, v)
    return np.sum(-Vq * v, axis=1)[:, np.newaxis] * (-Vq) + Wq * C + np.cross(C, -Vq)

def rotate_vec_opt(q, v):
    """Rotate or array of vectors v by quaternion q"""
    Wq = q[:,3]
    Vq = q[:,:3]
    
    s = np.empty(v.shape)
    s[:, 0] = Vq[:, 1] * v[:, 2] - Vq[:, 2] * v[:, 1]
    s[:, 1] = Vq[:, 2] * v[:, 0] - Vq[:, 0] * v[:, 2]
    s[:, 2] = Vq[:, 0] * v[:, 1] - Vq[:, 1] * v[:, 0]
    
    C = Wq * v + s
    
    nVq = -Vq
    s2 = np.empty(v.shape)
    s2[:, 0] = C[:, 1] * nVq[:, 2] - C[:, 2] * nVq[:, 1]
    s2[:, 1] = C[:, 2] * nVq[:, 0] - C[:, 0] * nVq[:, 2]
    s2[:, 2] = C[:, 0] * nVq[:, 1] - C[:, 1] * nVq[:, 0]
    
    return np.sum(-Vq * v, axis=1)[:, np.newaxis] * (-Vq) + Wq * C + s2


def toAxisAngle(q):
    r = np.empty_like(q)
    r[:, :3] = norm(q[:, :3])
    r[:, 3] = np.arccos(q[:, 3])*2
    return r

def power(q, t):
    """raise quaternion to the power of t"""
    n  = toAxisAngle(q)
    n[:, 3] = n[:, 3]*t
    return n 
    
def slerp(q, r, t):
    """spherical linear interpolation between q and r by t"""
#     return mult(power(mult(r, inv(q)), t), q)
    w =  q[:, 3]
    rw = r[:, 3]
    rv = r[:, :3]
    v =  q[:, :3]
    flCosOmega = w * rw + np.sum(rv*v, axis=1)# np.dot(rv, v)
    flSinOmega = np.sqrt(1 - flCosOmega*flCosOmega)
    flOmega = np.arctan2(flSinOmega, flCosOmega)
    flOneOverSinOmega = 1/flSinOmega
    k0 = sin((1-t)*flOmega) * flOneOverSinOmega
    k1 = sin(t*flOmega) * flOneOverSinOmega
    res = np.empty_like(q)
    res[:, 3] = w * k0 + rw * k1
    res[:, :3] = v * k0 + rv * k1;
    return res

class Rotator(object):

    """Quaternion based rotator implementation for theta, phi"""

    def __init__(self, q):
        self.q = q
        
    def __call__(self, thetas, phis, inverse=False):
        """
        Rotates the angles
        :param thetas: numpy array for thetas
        :param phis: numpy array for phis
        :param inverse: True if invserse rotation should be performed
        
        :returns theta, phi: the rotated angles
        """
        
        q = self.q if not inverse else inv(self.q)
        qv = sphere.dir2vec(thetas, phis)
        vec = rotate_vec_opt(q, qv)
        return sphere.vec2dir(vec)

class VecRotator(object):

    """Quaternion based rotator implementation for theta, phi"""

    def __init__(self, q):
        self.q = q
        
    def __call__(self, qv, inverse=False):
        """
        Rotates the angles
        :param gv: numpy array of x,y,z
        :param inverse: True if invserse rotation should be performed
        
        :returns theta, phi: the rotated angles
        """
        
        q = self.q if not inverse else inv(self.q)
        vec = rotate_vec_opt(q, qv)
        return sphere.vec2dir(vec)

