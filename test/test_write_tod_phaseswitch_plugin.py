'''
Created on Jan 14, 2014

@author: seehars
'''
import os
import tempfile

import pytest
import numpy as np
from ivy.utils.struct import Struct

from hide.plugins import write_tod_phaseswitch
from hide.strategy import center
from hide.utils import parse_datetime

class TestWriteTODPhaseswitchPlugin(object):

    plugin = None

    def setup(self):
        n_frequencies = 10
        params = Struct(file_fmt = "TEST_{mode}_{polarization}_{date}.h5",
                        strategy_start = "2015-01-01-00:00:00",
                        strategy_step_size = 1,
                        time_range = 5,
                        mode = 'MP',
                        polarizations = ['PXX'],
                        instrument = "hide.spectrometer.M9703A")
        
        tod = np.zeros((n_frequencies, 10))
        
        strategy_start = parse_datetime(params.strategy_start)
        self.ctx = Struct(params = params,
                          tod_vx = tod,
                          tod_vy = tod,
                          frequencies = np.arange(n_frequencies),
                          strategy_idx = 0,
                          strategy_start = strategy_start,
                          strategy_end = parse_datetime("2015-01-01-00:00:10"),
                          batch_start_date = strategy_start)

        dummy_strategy = center.load_strategy(self.ctx)
        self.ctx.strategy_coords = dummy_strategy
        
        self.plugin = write_tod_phaseswitch.Plugin(self.ctx)

    def test_write(self):
        output_path = tempfile.mkdtemp()
        t = self.ctx.batch_start_date.strftime(write_tod_phaseswitch.DATE_FORMAT)
        f = self.ctx.params.file_fmt.format(mode = self.ctx.params.mode,
                                            polarization = self.ctx.params.polarizations[0],
                                            date = t)
        self.ctx.params.output_path = output_path
        self.ctx.params.overwrite = False
        self.plugin()
        folder = '%04d/%02d/%02d'%(self.ctx.batch_start_date.year,
                                   self.ctx.batch_start_date.month,
                                   self.ctx.batch_start_date.day)
        file_path = os.path.join(output_path, folder, f)
        assert os.path.isfile(file_path)

        with pytest.raises(Exception):
            self.plugin()

        self.ctx.params.overwrite = True
        self.plugin()
        assert os.path.isfile(file_path)
        