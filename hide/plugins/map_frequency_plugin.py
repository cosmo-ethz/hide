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
Created on Dec 11, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals


class Plugin(object):
    '''
    Maps the frequencies to the plugin collection.
    '''
    
    def __init__(self, ctx):
        '''
        Constructor
        '''
        self.ctx = ctx
    
    def getWorkload(self):
        
        for idx, frequency in enumerate(self.ctx.frequencies):
#             gc.collect()
            ctx = self.ctx.copy()
            ctx.frequency = frequency
            ctx.frequency_idx = idx
            ctx.beam_profile = self.ctx.beam_profiles[idx]
            ctx.beam_norm = self.ctx.beam_norms[idx]
            del ctx.beam_profiles
            del ctx.beam_norms
            yield ctx