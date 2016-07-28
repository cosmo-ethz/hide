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
Created on Dec 9, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from hide.strategy import CoordSpec

def load_strategy(ctx):
    """
    Creates a dummy scanning strategy by always centering on RA/DEC 0/0
    
    :param ctx: The ctx instance with the paramterization
    
    :returns strategy: A dummy scanning strategy
    """
    
    start = ctx.strategy_start
    end   = ctx.strategy_end
    
    diff = int((end-start).total_seconds())
    step = ctx.params.strategy_step_size
    time = range(0, diff//step, step)
    return [CoordSpec(t, 0, 0, 0, 0) for t in time]