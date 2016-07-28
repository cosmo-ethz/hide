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
Created on Dec 16, 2015

author: seehars
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import h5py

from ivy.plugin.base_plugin import BasePlugin
from numpy import zeros, arange
import importlib

H5_FREQUENCY_NAME = "FREQUENCY"
H5_TIME_NAME = "TIME"

H5_P_GROUP_NAME = "P"
H5_P2_GROUP_NAME = "P2"
H5_PHASE0_NAME = "Phase0"
H5_PHASE1_NAME = "Phase1"
DATE_FORMAT = "%Y%m%d_%H%M%S"

class Plugin(BasePlugin):
    """
    Writes the time ordered phase switch data to the file system 
    """

    def __call__(self):
        tod_key = 'tod_v{pol}'
        # atm no kurtosis file is written
#         write_data(self.ctx, tod_key, H5_P_GROUP_NAME, H5_P2_GROUP_NAME)
        write_data(self.ctx, tod_key, H5_P_GROUP_NAME)

    def __str__(self):
        return "Write phase switch data to HDF5"
    
def write_data(ctx, tod_key, Pname, P2name = None):
    """
    Write the phase switch data to disk.
    
    :param ctx: instance of ivy context
    :param tod_key: key for the data to write
    :param Pname: group name for TOD
    :param P2name: group name for kurtosis data (None at the moment)
    """
    mod = importlib.import_module(ctx.params.instrument)
    if hasattr(mod, "convert_frequencies"):
        freq = mod.convert_frequencies(ctx.frequencies)
    else:
        freq = ctx.frequencies
    for pol in ctx.params.polarizations:
        file_path = get_path(ctx, pol)
        if os.path.exists(file_path):
            if ctx.params.overwrite:
                os.remove(file_path)
            else:
                raise IOError("File '%s' already exists!"%file_path)

        with h5py.File(file_path, 'w') as hdf_file:
            add_dataset(hdf_file, H5_FREQUENCY_NAME,freq)
#             time = asarray(ctx.strategy_coords)[:,0] * ctx.params.strategy_step_size
            time = arange(len(ctx.strategy_coords)) * ctx.params.strategy_step_size
            add_dataset(hdf_file, H5_TIME_NAME, time)
            
            grp = hdf_file.create_group(Pname)
            p1_p = ctx[tod_key.format(pol=pol[-1].lower())]
            
            # Second phase is only zeros
            p0_p = zeros(p1_p.shape)
            add_dataset(grp, H5_PHASE0_NAME, p0_p)
            add_dataset(grp, H5_PHASE1_NAME, p1_p)
            
            if P2name is not None:
                grp = hdf_file.create_group(P2name)
                # No kurtosis values atm
                p0_p2, p1_p2 = None, None
                add_dataset(grp, H5_PHASE0_NAME, p0_p2)
                add_dataset(grp, H5_PHASE1_NAME, p1_p2)

def get_path(ctx, pol):
    """
    Get path for output
    :param ctx: instance of ivy context
    :param pol: identifier for polarization
    """
    date = ctx.batch_start_date
    current = date.strftime(DATE_FORMAT)
    folder = "%04d/%02d/%02d"%(date.year, date.month, date.day)
    folder = os.path.join(ctx.params.output_path, folder)
    if not os.path.exists(folder):
        os.makedirs(folder)
    ff = ctx.params.file_fmt
    f = ff.format(mode=ctx.params.mode, polarization=pol,date=current)
    return os.path.join(folder,f)
    
def add_dataset(grp, name, data):
    """
    Adds a dataset to the group applying moderate compression
    
    :param grp: The group
    :param name: Name of the dataset
    :param data: the actual data to be added
    """
    grp.create_dataset(name, 
                       data=data, 
                       compression="gzip", 
                       compression_opts=4, 
                       shuffle=True)
