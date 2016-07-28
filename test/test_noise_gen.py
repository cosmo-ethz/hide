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
Created on Jan 12, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from scipy import stats
import numpy as np
from hide.utils import signal

class TestNoiseGen(object):

    def test_white_noise_gen(self):
        N=(1, 2**13)
        out = signal.noisegen(N=N, beta=0)
        out = out * 1./np.std(out) #rescale for KS(norm(0,1))
        assert out is not None
        assert out.shape == N
        D, p = stats.kstest(out[0], "norm")
        
        assert D < 0.015
