# Copyright (C) 2016 ETH Zurich, Institute for Astronomy

'''
Created on Feb 25, 2016

author: seehars
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from ivy.plugin.base_plugin import BasePlugin
from .write_tod_phaseswitch import get_path, add_dataset, H5_PHASE0_NAME, H5_PHASE1_NAME
import os
import h5py
from numpy import zeros

H5_RFI_GROUP_NAME = "RFI"

class Plugin(BasePlugin):
    """
    Writes the RFI contribution to the time ordered phase switch data to the
    file system. Works only after tod is written to disk.
    """

    def __call__(self):
        rfi_key = 'tod_v{pol}_rfi'
        write_data(self.ctx, rfi_key, H5_RFI_GROUP_NAME)

    def __str__(self):
        return "Write RFI data to HDF5"

def write_data(ctx, rfi_key, rfi_name):
    for pol in ctx.params.polarizations:
        file_path = get_path(ctx, pol)
        if os.path.exists(file_path):
            pass
        else:
            raise IOError("File '%s' doesn't exist, write TOD first!"%file_path)
        with h5py.File(file_path, 'r+') as hdf_file:
            grp = hdf_file.create_group(rfi_name)
            p0_p = ctx[rfi_key.format(pol=pol[-1].lower())]
            # Second phase is only zeros
            p1_p = zeros(p0_p.shape)
            add_dataset(grp, H5_PHASE0_NAME, p0_p)
            add_dataset(grp, H5_PHASE1_NAME, p1_p)
