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

import os

from ivy.plugin.base_plugin import BasePlugin
from datetime import datetime
import numpy as np

class Plugin(BasePlugin):
    """
    Writes the sources of the calibration days to disk 
    """

    def __call__(self):
        if not hasattr(self.ctx, "calibration"):
            return 

        calibration = self.ctx.calibration
        path = self.ctx.params.output_path
        name = self.ctx.params.calibration_file_fmt
        header = get_header()
        for date, entries in calibration.iteritems():
            write_day(date, entries, path, name, header)

    def __str__(self):
        return "Write calibration files to disk"
    
    
def write_day(date, entries, path, name, header):
    """
    Write calibration day to file
    
    :param date: key to calibration day
    :param entries: list of sources
    :param path: output_path
    :param name: name of calibaration file
    :param header: header information
    """
    path = get_path(path, date, name)
    line_format = '{time},{az},{el},Calibration: {source}\n'
    with open(path, 'w') as f:
        f.write(header)
        for entry in entries:
            f.write(line_format.format(time = entry.date.strftime('%H:%M:%S'),
                                       az = np.degrees(entry.az),
                                       el = np.degrees(entry.el),
                                       source = entry.src))

def get_path(path, date, name):
    """
    Get path for calibration day
    
    :param path: output_path
    :param date: key of calibration day
    :param name: name of calibration file
    """
    date = datetime.strptime(date, '%Y-%m-%d')
    folder = "%04d/%02d/%02d"%(date.year, date.month, date.day)
    folder = os.path.join(path, folder)
    if not os.path.exists(folder):
        os.makedirs(folder)
    outdate = date.strftime('%Y%m%d')
    f = name.format(date=outdate)
    return os.path.join(folder,f)
    
def get_header():
    """
    Get header for calibration day file
    """
    header = "# Calibration logfile antenna control system.\n"
    header += "# HH:MM:00,target-azimut,target-elevation,CALIBRATION: target.\n"
    header += "# Targetname should NOT contain spaces, otherwise they get lost...\n"
    return header