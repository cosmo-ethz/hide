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
Created on Sep 4, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from datetime import datetime, timedelta
import numpy as np

from ivy.plugin.base_plugin import BasePlugin
import os

HEADER = "Time,AzAntenna,ElAntenna,AzSource,ElSource,AzSpeedAnt,ElSpeedAnt,AzSpeedSrc,ElSpeedSrc, RA, DEC"
SEC_PER_DAY = 86400

class Plugin(BasePlugin):
    """
    Writes the time ordered data to the file system
    """

    def __call__(self):
        output_path = self.ctx.params.output_path
        file_fmt = self.ctx.params.coordinate_file_fmt
        
        file_date_fmt ="%04d%02d%02d"
        
        DAY = timedelta(1)
        
        strategy_start = self.ctx.strategy_start + timedelta(seconds=self.ctx.strategy[0].time)
        strategy_start = datetime(strategy_start.year, strategy_start.month, strategy_start.day)
        strategy_end = self.ctx.strategy_start + timedelta(seconds=self.ctx.strategy[-1].time)
        date = strategy_start
        
        idx0 = 0
        strategy = np.array(self.ctx.strategy)
        while strategy_start <= date <= strategy_end:
            next_day = date + DAY
            idx = np.sum(strategy[:, 0] < (next_day - self.ctx.strategy_start).total_seconds())
            if idx==idx0:
                date = next_day
                continue
                
            coords = strategy[idx0:idx]
            time = (coords[:, 0] - coords[0, 0]) / 3600
            
            time_steps = np.arange(time[0], time[-1]+self.ctx.params.coord_step_size/3600, self.ctx.params.coord_step_size/3600)
            
            elAntenna = np.interp(time_steps, time, np.degrees(coords[:, 1]))
            azAntenna = np.interp(time_steps, time, np.degrees(coords[:, 2]))
            
            filler = np.zeros((8, len(time_steps)))
            
            data = np.vstack((time_steps, azAntenna, elAntenna, filler)).T
            
            coord_path = os.path.join(output_path,
                                      "%04d"%date.year,
                                      "%02d"%date.month,
                                      "%02d"%date.day)
            
            if not os.path.exists(coord_path):
                os.makedirs(coord_path)

            file_name = file_fmt%(file_date_fmt%(date.year, date.month, date.day))
            np.savetxt(os.path.join(coord_path,file_name), 
                       data, 
                       fmt=str("%10.3f"), # numpy bug does not accept unicode 
                       delimiter=",", 
                       header=HEADER)
            
            idx0 = idx
            date = next_day
        
    def __str__(self):
        return "Write coord files"
    
