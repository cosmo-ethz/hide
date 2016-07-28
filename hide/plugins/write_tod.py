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
Created on Dec 8, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import h5py

from ivy.plugin.base_plugin import BasePlugin
from hide import DATE_FORMAT

TOD_VX_KEY = "TOD_VX"
TOD_VY_KEY = "TOD_VY"
TIME_AXIS_KEY = "time"
FREQUENCIES_AXIS_KEY = "frequencies"
STRATEGY_START_KEY = "strategy_start"
STRATEGY_END_KEY = "strategy_end"

class Plugin(BasePlugin):
    """
    DEPRECATED: Writes the time ordered data to the file system
    """

    def __call__(self):
#         start = datetime.strptime(self.ctx.params.strategy_start, DATE_FORMAT)
        
#         delta = self.ctx.strategy_idx * self.ctx.params.time_range * self.ctx.params.strategy_step_size
        current = self.ctx.batch_start_date.strftime(DATE_FORMAT) # start + timedelta(seconds= delta)
        file_name = self.ctx.params.file_fmt%current
        file_path = os.path.join(self.ctx.params.output_path, file_name)
        
        if os.path.exists(file_path):
            if self.ctx.params.overwrite:
                os.remove(file_path)
            else:
                raise IOError("File '%s' already exists!"%file_path)

        with h5py.File(file_path, "w") as hdf_file:
            hdf_file.create_dataset(TOD_VX_KEY, data=self.ctx.tod_vx)
            hdf_file.create_dataset(TOD_VY_KEY, data=self.ctx.tod_vy)
            
            hdf_file.create_dataset(TIME_AXIS_KEY, data=self.ctx.strategy_coords)
            hdf_file.create_dataset(FREQUENCIES_AXIS_KEY, data=self.ctx.frequencies)

            hdf_file.create_dataset(STRATEGY_START_KEY, data=current)
            strategy_end = self.ctx.strategy_end.strftime(DATE_FORMAT)
            hdf_file.create_dataset(STRATEGY_END_KEY, data=strategy_end)
            
    
    def __str__(self):
        return "Write data to HDF5"