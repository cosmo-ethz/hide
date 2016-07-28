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
Created on Mar 18, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

class Plugin(object):
    '''
    Combines the time ordered data for all frequencies
    '''

    def __init__(self, ctx):
        '''
        Constructor
        '''
        self.ctx = ctx
    
    def reduce(self, ctxList):
        tod_vx = []
        tod_vy = []
        for ctx in ctxList:
            tod_vx.append(ctx.signals)
        
        #TODO: no data for Y-Polarization
        tod_vx = np.array(tod_vx)
        tod_vy = np.array(tod_vy)
        self.ctx.tod_vx = tod_vx
        self.ctx.tod_vy = tod_vy