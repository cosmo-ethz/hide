# Copyright (C) 2016 ETH Zurich, Institute for Astronomy

'''
Created on Apr 22, 2016

author: seehars
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from ivy.plugin.base_plugin import BasePlugin
from hide.astro.gsm_point_src import add_point_sources

class Plugin(BasePlugin):

    def __call__(self):
        add_point_sources(self.ctx.frequency, 
                          self.ctx.params.beam_nside, 
                          self.ctx.astro_signal)
    
    def __str__(self):
        return "Add astro point sources"
   

