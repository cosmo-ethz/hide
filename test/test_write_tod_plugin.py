'''
Created on Jan 14, 2014

@author: jakeret, cchang
'''
import os
import tempfile

import pytest
import numpy as np
from ivy.utils.struct import Struct

from hide.plugins import write_tod
from hide.strategy import center
from hide.utils import parse_datetime



class TestWriteTODPlugin(object):

    plugin = None

    def setup(self):
        n_frequencies = 10
        params = Struct(file_fmt = "SKYMAP_%s.hdf",
                        strategy_start = "2015-01-01-00:00:00",
                        strategy_step_size = 1,
                        time_range = 5)
        
        tod = np.zeros((n_frequencies, 10))
        
        strategy_start = parse_datetime(params.strategy_start)
        self.ctx = Struct(params = params,
                          tod_vx=tod,
                          tod_vy=tod,
                          frequencies = np.arange(n_frequencies),
                          strategy_idx = 0,
                          strategy_start = strategy_start,
                          strategy_end   = parse_datetime("2015-01-01-00:00:10"),
                          batch_start_date = strategy_start)

        dummy_strategy = center.load_strategy(self.ctx)
        self.ctx.strategy_coords = dummy_strategy
        
        self.plugin = write_tod.Plugin(self.ctx)

    def test_write(self):
        output_path = tempfile.mkdtemp()
        
        self.ctx.params.output_path = output_path
        self.ctx.params.overwrite = False
        self.plugin()
        file_path = os.path.join(output_path, 
                                 "SKYMAP_"+self.ctx.params.strategy_start+".hdf")
        assert os.path.isfile(file_path)

        with pytest.raises(Exception):
            self.plugin()

        self.ctx.params.overwrite = True
        self.plugin()
        assert os.path.isfile(file_path)
        
