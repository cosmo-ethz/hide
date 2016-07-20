# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 11, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from ivy.utils.struct import Struct
from hide.plugins import reduce_frequency_plugin
import pytest

@pytest.skip("currently not used")
class TestReduceSignalsPlugin(object):

    def test_reduce(self):
        tod_vx = np.ones(10)
        ctx = Struct(tod_vx = tod_vx)
        
        ctx_count = 5
        ctxList = [ctx.copy() for _ in xrange(ctx_count)]
        
        plugin = reduce_frequency_plugin.Plugin(ctx)
        plugin.reduce(ctxList)
        
        assert ctx.tod_vx is not None
        assert ctx.tod_vx.shape == (ctx_count, 10)