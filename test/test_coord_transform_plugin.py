# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Jan 12, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

from ivy.utils.struct import Struct
from hide.plugins import coord_transform
from hide.beam import BeamSpec
from hide.strategy import CoordSpec

import healpy as hp
from hide.utils import sphere

class TestCoordTransformPlugin():
    
    def test_transform(self):
        nside = 2**4
        
        params = Struct(beam_nside = nside)
        
        strategy_coord = CoordSpec(0, 0, 0, 0, 0)
        
        beam_size = 0.041
        angles = np.arange(-1,1,10)*beam_size/2
        beam_spec = BeamSpec(angles, angles, 0)
        
        time_steps = 2
        
        idx = np.arange(hp.nside2npix(nside))
        thetas, phis = hp.pix2ang(nside, idx)
        tree = sphere.ArcKDTree(thetas, phis)
        
        ctx = Struct(params = params,
                     strategy_coords = [strategy_coord for _ in range(time_steps)],
                     beam_spec = beam_spec,
                     arc_tree = tree)

        
        plugin = coord_transform.Plugin(ctx)
        plugin()
        
        assert ctx.beams is not None
        assert len(ctx.beams) == time_steps
        
