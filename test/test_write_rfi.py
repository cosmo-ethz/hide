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
Created on Feb 26, 2016

@author: seehars
'''
import os
import tempfile

import numpy as np
from ivy.utils.struct import Struct

from hide.plugins import write_tod_phaseswitch, write_rfi
from hide.utils import parse_datetime
import h5py

def test_write():
    output_path = tempfile.mkdtemp()
    n_frequencies, n_time = 10, 10
    params = Struct(file_fmt = "TEST_{mode}_{polarization}_{date}.h5",
                    strategy_start = "2015-01-01-00:00:00",
                    strategy_step_size = 1,
                    time_range = 5,
                    mode = 'MP',
                    polarizations = ['PXX'],
                    output_path = output_path,
                    instrument = "hide.spectrometer.M9703A")
        
    tod = np.zeros((n_frequencies, n_time))
    strategy = range(n_time)
    strategy_start = parse_datetime(params.strategy_start)
    ctx = Struct(params = params,
                 tod_vx = tod,
                 tod_vx_rfi = tod,
                 frequencies = np.arange(n_frequencies),
                 strategy_start = strategy_start,
                 batch_start_date = strategy_start,
                 strategy_coords = strategy)

    todplugin = write_tod_phaseswitch.Plugin(ctx)
    f = write_tod_phaseswitch.get_path(ctx, 'PXX')
    todplugin()
    rfiplugin = write_rfi.Plugin(ctx)
    rfiplugin()
    assert os.path.isfile(f)
    with h5py.File(f) as F:
        t = F[write_tod_phaseswitch.H5_P_GROUP_NAME][write_tod_phaseswitch.H5_PHASE0_NAME][:]
        r = F[write_rfi.H5_RFI_GROUP_NAME][write_tod_phaseswitch.H5_PHASE0_NAME][:]
        assert np.all(t == r)
    