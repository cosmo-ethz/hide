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
Created on Sep 14, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from ivy.plugin.base_plugin import BasePlugin

class Plugin(BasePlugin):
    """
    Cleans up the context to avoid a memory leak
    """

    def __call__(self):
        del self.ctx.tod_vx
        del self.ctx.tod_vy
        del self.ctx.frequencies
        del self.ctx.strategy_coords
        del self.ctx.beams
        del self.ctx.tod_vx_rfi 
        
    def __str__(self):
        return "Clean up"
    
