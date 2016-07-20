# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Apr 25, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import pkgutil
import numpy as np
import pytest

from ivy.utils.struct import Struct

from hide.beam import BeamSpec
from hide.beam import top_hat
from hide.beam import gaussian
from hide.beam import gaussian_interp
from hide.beam import airy_disk
from hide import beam

EPS = np.array([[1e-6]], dtype=np.float64)

@pytest.fixture()
def params():
    params = Struct(beam_elevation = 4.461,
                    beam_azimut = 4.461,
                    beam_frequency_min = 1000,
                    beam_frequency_max = 1003,
                    beam_frequency_pixscale = 1,
                    beam_pixscale = 0.02,
                    beam_response = 1,
                    speed_of_light = 299792.458, #TODO check
                    dish_diameter = 3.5,
                    beam_nside = 64
                    )
    return params

@pytest.fixture()
def beam_spec(params):
    beam_elevation = np.radians(params.beam_elevation)
    beam_azimut = np.radians(params.beam_azimut)
    
    theta = np.linspace(-beam_elevation/2, beam_elevation/2, 50)
    phi = theta
    beam_spec = BeamSpec(phi, theta, 0)
    return beam_spec

@pytest.fixture()
def frequencies(params):
    frequencies = np.arange(params.beam_frequency_min, params.beam_frequency_max, params.beam_frequency_pixscale)
    return frequencies


def test_beam_providers(params, beam_spec, frequencies):
    params.speed_of_light = 299792458
    for importer, modname, ispkg in pkgutil.iter_modules(beam.__path__):
        mod = importer.find_module(modname).load_module(modname)
        print(modname)
        beam_profiles, _ = mod.load_beam_profile(beam_spec, frequencies, params)
        assert beam_profiles is not None
        assert len(beam_profiles) == len(frequencies)
        
        for beam_profile in beam_profiles:
            peak = beam_profile(EPS, EPS)
            assert np.allclose(peak, 1.0, 1e-3)
                 
        

class TestTopHatBeamProvider(object):

    def test_load_beam_profile(self, params, beam_spec, frequencies):
        beam_profiles, beam_norms = top_hat.load_beam_profile(beam_spec, frequencies, params)
        
        assert beam_profiles is not None
        assert beam_norms is not None
        assert len(beam_profiles) == len(frequencies)
        assert len(beam_norms) == len(frequencies)
        
        X,Y = np.meshgrid(beam_spec.ra, beam_spec.dec)
        for beam_profile in beam_profiles:
            profile = beam_profile(X,Y)
            #at least the edges should be 0
            assert profile[0,0] == 0
            assert profile[params.beam_elevation-1,0] == 0
            assert profile[0,params.beam_azimut-1] == 0
            assert profile[params.beam_elevation-1,params.beam_azimut-1] == 0
            assert profile[len(beam_spec.ra)//2, len(beam_spec.dec)//2] != 0
            
            
class TestGaussianBeamProvider(object):

    def test_load_beam_profile(self, params, beam_spec, frequencies):
        beam_profiles, beam_norms = gaussian.load_beam_profile(beam_spec, frequencies, params)

        assert beam_profiles is not None
        assert beam_norms is not None
        assert len(beam_profiles) == len(frequencies)
        assert len(beam_norms) == len(frequencies)
        
        X,Y = np.meshgrid(beam_spec.ra, beam_spec.dec)
        for beam_profile in beam_profiles:
            profile = beam_profile(X,Y)
            assert np.allclose(profile[0,0], 0.0, atol=1e-4)
            assert np.allclose(profile[params.beam_elevation-1,0], 0.0, atol=1e-4)
            assert np.allclose(profile[0,params.beam_azimut], 0.0, atol=1e-4)
            assert np.allclose(profile[params.beam_elevation-1,params.beam_azimut-1], 0.0, atol=1e-4)
            
            assert profile[len(beam_spec.ra)//2, len(beam_spec.dec)//2] != 1
            
            
class TestGaussianInterpBeamProvider(object):

    def test_load_beam_profile(self, params, beam_spec, frequencies):
        beam_profiles, beam_norms = gaussian_interp.load_beam_profile(beam_spec, frequencies, params)

        assert beam_profiles is not None
        assert beam_norms is not None
        assert len(beam_profiles) == len(frequencies)
        assert len(beam_norms) == len(frequencies)
        
        X,Y = np.meshgrid(beam_spec.ra, beam_spec.dec)
        for beam_profile in beam_profiles:
            profile = beam_profile(X,Y)
            assert np.allclose(profile[0,0], 0.0, atol=1e-4)
            assert np.allclose(profile[params.beam_elevation-1,0], 0.0, atol=1e-4)
            assert np.allclose(profile[0,params.beam_azimut], 0.0, atol=1e-4)
            assert np.allclose(profile[params.beam_elevation-1,params.beam_azimut-1], 0.0, atol=1e-4)
            
            assert profile[len(beam_spec.ra)//2, len(beam_spec.dec)//2] != 1

class TestAiryDiskBeamProvider(object):

    def test_load_beam_profile(self, params, beam_spec, frequencies):
        beam_profiles, beam_norms = airy_disk.load_beam_profile(beam_spec, frequencies, params)

        assert beam_profiles is not None
        assert beam_norms is not None
        assert len(beam_profiles) == len(frequencies)
        assert len(beam_norms) == len(frequencies)
        
        X,Y = np.meshgrid(beam_spec.ra, beam_spec.dec)
        for beam_profile in beam_profiles:
            profile = beam_profile(X,Y)
            assert np.allclose(profile[0,0], 0.0, atol=1e-4)
            assert np.allclose(profile[params.beam_elevation-1,0], 0.0, atol=1e-4)
            assert np.allclose(profile[0,params.beam_azimut], 0.0, atol=1e-4)
            assert np.allclose(profile[params.beam_elevation-1,params.beam_azimut-1], 0.0, atol=1e-4)
            
            assert profile[len(beam_spec.ra)//2, len(beam_spec.dec)//2] != 1

