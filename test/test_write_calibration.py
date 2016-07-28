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
Created on Mar 29, 2016

author: seehars
'''
from __future__ import print_function, division, absolute_import, unicode_literals
from hide.plugins import write_calibration

import os
import numpy as np
from ivy.utils.struct import Struct
import tempfile
from datetime import datetime
from hide.strategy.scheduler import ScheduleEntry

class TestWriteCalibrationPlugin(object):
    
    def test_write_calibration(self):
        path = tempfile.mkdtemp()
        
        file_fmt = "test{date}.txt"
        params = Struct(
                        output_path=path,
                        calibration_file_fmt=file_fmt
                        )
        
        date = datetime(year=2015,month=1,day=1)
        calibration = {date.strftime('%Y-%m-%d'): [ScheduleEntry(date, 0., 1., 'Calibration: Test')]}
        ctx = Struct(params=params,
                     calibration=calibration 
                     )
        
        plugin = write_calibration.Plugin(ctx)
        plugin()
        
        cal_path =  os.path.join(params.output_path, 
                                 date.strftime('%Y'),
                                 date.strftime('%m'),
                                 date.strftime('%d'),
                                 "test20150101.txt")
        
        with open(cal_path, 'r') as f:
            lines = list(f)
            assert len(lines) == 4
            cal = lines[-1].split(',')
            assert cal[0] == date.strftime('%H:%M:%S')
            assert np.isclose(float(cal[1]), 0.)
            assert np.isclose(float(cal[2]), np.degrees(1.))
            assert cal[3] == 'Calibration: Test\n'
                