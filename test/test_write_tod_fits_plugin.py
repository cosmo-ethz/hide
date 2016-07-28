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
Created on Sep 7, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import tempfile
from datetime import datetime

import pytest
import numpy as np
from astropy.io import fits
from ivy.utils.struct import Struct

from hide.plugins import write_tod_fits
from hide import DATE_FORMAT


ROOT_PATH = os.path.join(os.path.dirname(__file__), "res")
FITS_PATH = os.path.join(ROOT_PATH, "HIMap_20150504_175242_02.fit.gz")


class TestWriteTODPlugin(object):
    
    def setup(self):
        params = Struct(strategy_start = "2015-01-01-00:00:00",
                        strategy_end   = "2015-01-01-00:00:10",
                        file_fmt = "SKYMAP_%s.fit",
                        strategy_step_size=1
                        )
        
        hdu = fits.open(FITS_PATH)
        primaryHDU, binTableHDU = hdu
        
        self.tod = primaryHDU.data
        self.frequencies = binTableHDU.data["FREQUENCY"][0]
        
        self.ctx = Struct(params = params,
                          tod_vx=self.tod,
                          tod_vy=self.tod,
                          frequencies = self.frequencies,
                          batch_start_date = datetime.strptime(params.strategy_start, 
                                                               DATE_FORMAT))

        self.plugin = write_tod_fits.Plugin(self.ctx)

    def test_write(self):
        pytest.skip("Plugin deprecated and no compatible with newest astropy")
        output_path = tempfile.mkdtemp()
        
        self.ctx.params.output_path = output_path
        self.ctx.params.overwrite = False
        self.plugin()
        
        file_path = os.path.join(output_path, 
                                 "2015",
                                 "01",
                                 "01",
                                 "SKYMAP_20150101_000000.fit")
        assert os.path.isfile(file_path)
        
        hdu = fits.open(file_path)
        primaryHDU, binTableHDU = hdu
        assert np.all(self.tod == primaryHDU.data)
        assert np.all(self.frequencies[::-1] == binTableHDU.data["FREQUENCY"])
        
        assert primaryHDU.header[write_tod_fits.DATE_OBS_KEY] == "2015/01/01"
        assert primaryHDU.header[write_tod_fits.TIME_OBS_KEY] == "00:00:00.000"
        assert primaryHDU.header[write_tod_fits.TIME_STEP_KEY] == 1
        

        with pytest.raises(Exception):
            self.plugin()

        self.ctx.params.overwrite = True
        self.plugin()
        assert os.path.isfile(file_path)
        

