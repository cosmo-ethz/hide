
# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

"""
Tests for `hide` module.
"""
from __future__ import print_function, division, absolute_import

import pytest
import tempfile
import ivy
import os

try:
    os.environ["HUDSON_URL"]
    JENKINS = True
except KeyError:
    JENKINS = False

class TestSampleRun(object):

    def test_sampleRun(self):
        if JENKINS:
            pytest.skip("Only for local testing")
            
        output_path = tempfile.mkdtemp()
        
        args = ["--output-path="+output_path,
#                 "--beam-frequency-min=980",
#                 "--beam-frequency-max=1080",
#                 "--astro-signal-provider=hide.astro.gsm",
#                 "--scanning-strategy-provider=hide.strategy.full_sky",
#                 "--beam-nside=32",
#                 "--beam-frequency-pixscale=1",
                "--strategy-start=2015-12-16-00:00:00",
                "--strategy-end=2015-12-16-23:59:00",
                "--backend=sequential",
                "hide.config.bleien7m"]
        
        ivy.execute(args)
        
