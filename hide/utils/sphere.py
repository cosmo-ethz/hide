# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 22, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from numpy import arccos
from scipy import spatial
import healpy as hp

from hide.utils import sin_cos
import ephem

def dec2theta(dec):
    return (-dec + np.pi/2)

def ra2phi(ra):
    return ra #(ra + np.pi)

def theta2dec(theta):
    return (-theta + np.pi/2)

def phi2ra(phi):
    return phi # (phi) - np.pi

def vec2dir(vec):
    """converts vector to angles"""
    vx = vec[:,0]
    vy = vec[:,1]
    vz = vec[:,2]
#     r = np.sqrt(vx**2+vy**2+vz**2)
    r = np.sqrt(np.sum(np.square(vec), axis=1))
#     assert np.all(r==r2)
    ang = np.empty((2, r.size))
    ang[0, :] = arccos(vz / r)
    ang[1, :] = np.arctan2(vy, vx)
    return ang.squeeze()

def dir2vec(theta, phi):
    """converts angle to vector"""
    sin_t, cos_t = sin_cos(theta) #sin(theta), cos(theta)
    sin_p, cos_p = sin_cos(phi) #sin(phi), cos(phi)
    vec = np.empty((len(theta), 3))
    vec[:,0] = sin_t * cos_p
    vec[:,1] = sin_t * sin_p
    vec[:,2] = cos_t
    return vec


def separation(d1, a1, d2, a2):
    """
    great circle distance http://en.wikipedia.org/wiki/Great-circle_distance#Computational_formulas
    
    :param d1: dec 1
    :param a1: ra 1
    :param d2: dec 2
    :param a2:ra 2
    """
    
    sin_d1, cos_d1 = np.sin(d1), np.cos(d1) #sin_cos(d1) #np.sin(d1), np.cos(d1)
    sin_d2, cos_d2 = np.sin(d2), np.cos(d2) #sin_cos(d2) #np.sin(d2), np.cos(d2)
    sin_a2a1, cosa2a1 = np.sin(a2-a1), np.cos(a2-a1) #sin_cos(a2-a1) #np.sin(a2-a1), np.cos(a2-a1)
    return (np.arctan2((np.sqrt(cos_d2**2 * sin_a2a1**2 + (cos_d1 * sin_d2 - sin_d1 * cos_d2 * cosa2a1)**2)), (sin_d1 * sin_d2 + cos_d1 * cos_d2 * cosa2a1)))

class ArcKDTree(object):
    """Wraps the scipy.spatial.cKDTree such that the tree can be used with spherical coords"""
    def __init__(self, theta, phi):
        self.tree = spatial.cKDTree(dir2vec(theta, phi))

    def query_ball_point(self, theta, phi, r, eps=0):
        return self.tree.query_ball_point(dir2vec(np.atleast_1d(theta), np.atleast_1d(phi))[0], 
                                          r, 
                                          p=2, 
                                          eps=eps)

    def query(self, theta, phi, k=1, eps=0, p=2, distance_upper_bound=np.inf):
        """
        Query the kd-tree for nearest neighbors using theta, phi
        :param theta:
        :param phi:
        :param k:
        :param eps:
        :param p:
        :param distance_upper_bound:
        
        :returns d, i: The distances to the nearest neighbors,  the locations of the neighbors in self.data.
        """
        x = dir2vec(np.atleast_1d(theta), np.atleast_1d(phi))[0]
        return self.tree.query(x, k)

def get_observer(ctx):
    obs = ephem.Observer()
    obs.lon = str(ctx.params.telescope_longitude)
    obs.lat = str(ctx.params.telescope_latitude)
    obs.elevation = 500
    obs.pressure = 0
    return obs

def radec_to_altaz(date, ra, dec, obs=None, ctx=None):
    if obs is None:
        obs = get_observer(ctx)
    obs.date = (date.year, date.month, date.day, date.hour, date.minute, date.second)
    body = ephem.FixedBody()
    body._ra = ra
    body._dec = dec
    body.compute(obs)
    return body.alt, body.az
    
def altaz_to_ra_dec(date, az, alt, obs=None, ctx=None):
    if obs is None:
        obs = get_observer(ctx)
    obs.date = (date.year, date.month, date.day, date.hour, date.minute, date.second)
    
    return obs.radec_of(az, alt)

def rotate_map(Map, rotator, mask = None):
    """
    Map is map in system A
    rotator is rotator from system B to A
    mask is a mask in system B
    returns new map in system B
    """
    npix = Map.shape[0]
    nside = hp.npix2nside(npix)
    thetas, phis = hp.pix2ang(nside, np.arange(npix))
    rts, rps = rotator.I(thetas, phis)
    vals = hp.pixelfunc.get_interp_val(Map, rts,  rps)
    nm = vals
    if mask == None:
        return nm
    else:
        nm = hp.ma(nm)
        nm.mask = mask
        return nm