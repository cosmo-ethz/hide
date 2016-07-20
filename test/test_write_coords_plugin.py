# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Sep 4, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals
from hide.plugins import write_coords

import os
import numpy as np
from ivy.utils.struct import Struct
from hide.strategy import drift_scan
import tempfile
from hide.utils import parse_datetime

ROOT_PATH = os.path.join(os.path.dirname(__file__), "res")
COORDS_PATH = os.path.join(ROOT_PATH, "coords", "coord5m20141121.txt")


class TestWriteCoordsPlugin(object):
    
    def test_write_coords(self):
        path = tempfile.mkdtemp()
        
        params = Struct(telescope_latitude = 47.344192,
                        telescope_longitude = 8.114368,
                        alt_delta = 3.5,
                        azimuth_pointing = 181,
                        altitude_start_pos = 41.0,
                        altitude_max_pos = 90.0,
                        strategy_step_size = 1,
                        
                        coord_step_size = 1,
                        output_path = path,
                        coordinate_file_fmt = "coord7m%s.txt"
                        )
        
        ctx = Struct(params=params,
                     strategy_start = parse_datetime("2015-01-01-00:00:00"),
                     strategy_end   = parse_datetime("2015-01-02-00:01:00")
                     )
        
        strategy = drift_scan.load_strategy(ctx)
        
        ctx.strategy = strategy
        plugin = write_coords.Plugin(ctx)
        plugin()
        
        coord_path =  os.path.join(params.output_path, 
                                   "2015",
                                   "01",
                                   "01",
                                   "coord7m20150101.txt")
        
        coords = np.genfromtxt(coord_path, delimiter = ',', names = True)
        assert len(coords) == write_coords.SEC_PER_DAY / int(params.coord_step_size)
        
        strategy_arr = np.asarray(strategy)
        N = len(coords)
        assert np.allclose(strategy_arr[:N, 1], np.radians(coords["ElAntenna"]))
        
        coord_path =  os.path.join(params.output_path, 
                                   "2015",
                                   "01",
                                   "02",
                                   "coord7m20150102.txt")
        
        coords = np.genfromtxt(coord_path, delimiter = ',', names = True)
        assert len(coords) == 60 / int(params.coord_step_size)
        