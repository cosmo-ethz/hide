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
    Combines all signals to time ordered data
    '''


    def __init__(self, ctx):
        '''
        Constructor
        '''
        self.ctx = ctx
    
    def reduce(self, ctxList):
        tod_vx = []
        for ctx in ctxList:
            tod_vx.append(ctx.signal)
        
        tod_vx = np.array(tod_vx)
        self.ctx.tod_vx = tod_vx