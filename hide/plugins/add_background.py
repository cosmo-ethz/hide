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
Created on Mar 23, 2016

author: seehars
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from ivy.plugin.base_plugin import BasePlugin

import importlib
import numpy as np

class Plugin(BasePlugin):
    """
    Adds a time-constant, elevation dependent background to the TOD.
    """

    def __call__(self):
        #load module
        mod = importlib.import_module(self.ctx.params.instrument)
        
        #delegate loading of background as a function of elevation
        bg_model = mod.get_background(self.ctx.frequencies,
                                      self.ctx.params.elevation_model)
        
        # get all elevations from strategy (in radians)
        els = np.asarray(self.ctx.strategy_coords)[:,1]
        #add background to TOD
        #TODO: no background for Y-polarization
        self.ctx.tod_vx += bg_model(els)
    
    def __str__(self):
        return "Adding background to TOD"
