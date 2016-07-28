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

import numpy as np

from ivy.plugin.base_plugin import BasePlugin
from hide.utils import parse_datetime


class Plugin(BasePlugin):
    """
    Initialize  ..,
    
    """

    def __call__(self):
        np.random.seed(self.ctx.params.seed)
        self.ctx.strategy_start = parse_datetime(self.ctx.params.strategy_start)
        self.ctx.strategy_end   = parse_datetime(self.ctx.params.strategy_end)
                                                    
    def __str__(self):
        return "Initialize"