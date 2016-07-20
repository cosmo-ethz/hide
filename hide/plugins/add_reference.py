# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 8, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

from ivy.plugin.base_plugin import BasePlugin


class Plugin(BasePlugin):

    def __call__(self):
        pass
    
    def __str__(self):
        return "Add reference"