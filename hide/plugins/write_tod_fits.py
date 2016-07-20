# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Sep 4, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import numpy as np
from astropy.io import fits
from ivy.plugin.base_plugin import BasePlugin

FITS_FILE_DATE_FMT = "%Y%m%d_%H%M%S"
FITS_DATE_FMT = "%Y/%m/%d"
FITS_TIME_FMT = "%H:%M:%S.000"
TIME_OBS_KEY = "TIME-OBS"
DATE_OBS_KEY = "DATE-OBS"
TIME_STEP_KEY = "CDELT1"

class Plugin(BasePlugin):
    """
    Writes the time ordered data to the file system in a fits file
    """

    def __call__(self):
        batch_start_date = self.ctx.batch_start_date
        output_path = self.ctx.params.output_path
        
        data_path = os.path.join(output_path,
                                "%04d"%batch_start_date.year, 
                                "%02d"%batch_start_date.month, 
                                "%02d"%batch_start_date.day)
        
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        
        current = batch_start_date.strftime(FITS_FILE_DATE_FMT)
        file_name = self.ctx.params.file_fmt%current
        
        file_path = os.path.join(data_path, file_name)

        if os.path.exists(file_path):
            if self.ctx.params.overwrite:
                os.remove(file_path)
            else:
                raise IOError("File '%s' already exists!"%file_path)

        header =fits.Header()
        header[DATE_OBS_KEY] = batch_start_date.strftime(FITS_DATE_FMT)
        header[TIME_OBS_KEY] = batch_start_date.strftime(FITS_TIME_FMT)
        header[TIME_STEP_KEY] = self.ctx.params.strategy_step_size
        
        primary = fits.PrimaryHDU(data=self.ctx.tod_vx,
                                  header=header)
        
        freq_format = "%iD8.3"%(len(self.ctx.frequencies))
        columns = fits.ColDefs([fits.Column("TIME", format = '3600D8.3'),
                                fits.Column("FREQUENCY", format = freq_format, 
                                            array = np.atleast_2d(self.ctx.frequencies[::-1]))
                       ])
        
        hduList = fits.HDUList([primary,
                        fits.BinTableHDU.from_columns(columns)])
        
        hduList.writeto(file_path)


    def __str__(self):
        return "Write data to fits"
    
