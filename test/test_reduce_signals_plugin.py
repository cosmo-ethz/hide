# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 11, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from ivy.utils.struct import Struct
from hide.plugins import reduce_signals_plugin


class TestReduceSignalsPlugin(object):

    def test_reduce(self):
        ctx = Struct(signal = 1)
        
        ctx_count = 5
        ctxList = [ctx.copy() for _ in xrange(ctx_count)]
        
        plugin = reduce_signals_plugin.Plugin(ctx)
        plugin.reduce(ctxList)
        
        assert ctx.tod_vx is not None
        assert ctx.tod_vx.shape == (ctx_count, )