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
Created on Apr 25, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from hide.beam import airy

def load_beam_profile(beam_spec, frequencies, params):
    """
    Creates a 2d airy disk beam profile for the given params definition 
    
    :param params: The params instance with the paramterization
    
    :returns profile: A list of callable beam profiles
    """

    beam_profiles = []
    beam_norms = []
    for frequency in frequencies:
        la = params.speed_of_light / (frequency * 10**6)
        fwhm = 1.22 * la / params.dish_diameter
        beam_profiles.append(airy.airy_wrapper(fwhm))
        beam_norms.append(airy.normalization(fwhm, params.beam_nside))
    return beam_profiles, beam_norms
