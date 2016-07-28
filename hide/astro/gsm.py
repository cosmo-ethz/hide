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
Created on Feb 26, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import glob
import os
from pkg_resources import resource_filename

import healpy as hp
import numpy as np

import hide

GSM_FILE_PATH = "Radio/global_sky_model/maps"
GSM_FILE_PATH = "data/gsm/maps"


gsm_maps = None

def _load_files():
    root_file_path = resource_filename(hide.__name__, GSM_FILE_PATH)
    
    nside_files_path = glob.glob(root_file_path+"/*")
    maps = {}
    for nside_file_path in nside_files_path:
        try:
            nside = int(nside_file_path.split("/")[-1])
        
            file_paths = np.array(glob.glob(os.path.join(root_file_path, "%s"%nside, "*")))
            
            frequencies = []
            for file_path in file_paths:
                file_name = file_path.split("/")[-1]
                freq = file_name.split("_")[-1][:-5]
                frequencies.append(float(freq))
            
            idx = np.argsort(frequencies)
            maps[int(nside)] = (np.array(frequencies)[idx], file_paths[idx])
        except Exception: continue
        
    global gsm_maps
    gsm_maps = maps

def load_signal(ctx):
    """
    Returns an interpolated global sky model (GSM) map dependent on the frequency.
    
    :param params: The ctx instance with the paramterization
    :returns signal: The astro signal
    """
    if gsm_maps is None:
        _load_files()
        
    gsm_frequencies, gsm_file_paths = gsm_maps[ctx.params.beam_nside]
    
    assert ctx.frequency >= gsm_frequencies[0], "Frequency (%s) outside available frequencies (%s - %s)"%(ctx.frequency, 
                                                                                                          gsm_frequencies[0], 
                                                                                                          gsm_frequencies[-1])
    assert ctx.frequency <= gsm_frequencies[-1], "Frequency (%s) outside available frequencies (%s - %s)"%(ctx.frequency, 
                                                                                                           gsm_frequencies[0], 
                                                                                                           gsm_frequencies[-1])
    
    
    for i, frequency in enumerate(gsm_frequencies):
        if ctx.frequency < frequency:
            break
    
    lf_file = gsm_file_paths[i-1]
    uf_file = gsm_file_paths[i]
    diff = (frequency - ctx.frequency) / (frequency - gsm_frequencies[i-1])
    
    lf_map = hp.read_map(lf_file, verbose=False)
    uf_map = hp.read_map(uf_file, verbose=False)
    
    gsm_map = diff * lf_map + (1-diff) * uf_map
    
    return gsm_map