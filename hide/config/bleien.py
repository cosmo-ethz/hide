# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 8, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals
from ivy.plugin.parallel_plugin_collection import ParallelPluginCollection

plugins = ["hide.plugins.initialize",
           "hide.plugins.load_beam_profile",
           "hide.plugins.scanning_strategy",
           "hide.plugins.write_coords",
           ParallelPluginCollection([
                                    "hide.plugins.qu_opt_coord_transform",
                                     ParallelPluginCollection([
                                                            "hide.plugins.astro_signal",
                                                            "hide.plugins.earth_signal",
                                                            "hide.plugins.combine_signals",
                                                             ],
                                                            "hide.plugins.map_frequency_plugin",
                                                            "hide.plugins.reduce_frequency_plugin", 
#                                                             parallel=False
                                                            ),
                                    "hide.plugins.apply_gain",
                                    "hide.plugins.add_rfi",
                                    "hide.plugins.background_noise",
                                    "hide.plugins.add_reference",
                                    "hide.plugins.write_tod_fits",
                                    "hide.plugins.clean_up",
                                     ],
                                    "hide.plugins.map_strategy_plugin",
                                    #"hide.plugins.reduce_signals_plugin",
                                    ),
           
            "ivy.plugin.show_summary_stats"
          ]


from hide.config import common

for name in [name for name in dir(common) if not name.startswith("__")]:
    globals()[name] = getattr(common, name)

# ==================================================================
# O U T P U T
# ==================================================================
output_path = "."                           # path to output folder
overwrite = False                           # True if file should be overwritten 
file_fmt = "SKYMAP_%s.fit"                  # data file name format
coordinate_file_fmt = "coord7m%s.txt"       # coordinate file name format


# ==================================================================
# T E L E S C O P E
# ==================================================================
#-----------------
# B L E I E N
#-----------------
# telescope_latitude = 47.344192
# telescope_longitude = 8.114368
telescope_latitude = 47.3412278
telescope_longitude = 8.112215

# ==================================================================
# B E A M
# ==================================================================
beam_profile_provider = "hide.beam.airy"
beam_elevation = 8.4                      # elevation [degree]
beam_azimut = 8.4                         # azimuth [degree]
beam_pixscale = 0.2                         # pixel scale (degree/pixel)
beam_frequency_min = 980                    # minimum frequency: [MHz]
beam_frequency_max = 1280                   # maximum frequency: [MHz]
beam_frequency_pixscale = 50 #0.05          # pixel scale (frequency/pixel)
beam_response = 1                           # response [0..1]
beam_nside = 64                             # healpix NSIDE
dish_diameter = 5.0                         # diameter of the dish [m]

# ==================================================================
# S C A N N I N G  S T R A T E G Y
# ==================================================================
scanning_strategy_provider = "hide.strategy.drift_scan" 
strategy_start = "2015-01-01-00:00:00"      # survey start time. Format YYYY-mm-dd-HH:MM:SS
strategy_end   = "2015-01-01-0:59:00"       # survey end time. Format YYYY-mm-dd-HH:MM:SS
strategy_step_size = 1                      # size of step in [sec]
time_range = 900                            # time range per file [sec]
coord_step_size = 2.5                       # step size in the coords file
# -------------------
# D R I F T  S C A N
# -------------------
alt_delta = 3.5                             # change in altitude per day (drift scan) [degree]
azimuth_pointing = 181                      # pointing direction in azimuth direction [degree]
altitude_start_pos = 41.0                   # start position in altitude direction [degree]
altitude_max_pos = 90.0                     # max position in altitude direction [degree]


# ==================================================================
# A S T R O
# ==================================================================
astro_signal_provider = "hide.astro.static_gsm"
astro_flux = 5.0                            # galactic + cosmological signal [K]

cache_astro_signals = True                  # flag if loaded signals per frequency should be kept in memory

# ==================================================================
# E A R T H
# ==================================================================
earth_signal_provider = "hide.earth.constant"


# -------------------
# c o n s t a n t 
# -------------------
earth_signal_flux = 0                       # flux of constant earth signal

# -------------------
# h o r i z o n
# -------------------
vmin = -0.7                                 # lower end of model [rad]
vmax = 0.9                                  # upper end of model [rad]

fit_coeffs = [ 35.12304423, 
              -44.5904649,  
               -8.04977763,  
               27.37012328,
               -4.33814833,
               -6.06838216,
                1.85068615,
                0.87829086,
                0.13266224]


# ==================================================================
# N O I S E
# ==================================================================
load_noise_template = False
white_noise_scale = 0.1318                 # white noise scale
color_noise_amp = 0.0162                   # amplitude of colored noise
color_noise_beta = 1.0517                  # 1/f^beta factor


# ==================================================================
# P O S T P R O C E S S I N G
# ==================================================================
instrument = "hide.spectrometer.callisto"    # spectrometer specific gain implementation


log_base = 5                                # base when logarithmizing the TOD
offset_baseline = 145                       # offset added to TOD
model_sw = [206.14434317-37.49241937j,
            37.55385581+36.8715066j,
            56.08776437+33.31747476j,
            12.71640072+14.50377746j,
            -13.07603458+46.72096541j,
            58.16003837 -5.33708575j,
            -119.32754311+63.03311147j,
            316.71933105+10.19877621j,
            13.48476887+13.05673126j]
model_fmin = 998.812011719
model_fmax = 1256.06201172
model_nf = 180
model_slope = -0.053047240811


# ==================================================================
# R F I
# ==================================================================

#bursts
max_rfi_count = 20                          # maximal rfi bursts per hour
coeff_freq = [0.179, 1.191]                 # poly coeffs for frequency sigma
coeff_time = [0.144, -1.754, 63.035]        # poly coeffs for time sigma
sigma_range = 3.0                           # no of sigmas to take into account
amp_scale = 3                               # scale of lognorm for amplitude
amp_loc = 0                                 # loc of lognorm for amplitude

#constant
rfi_freqs = [25, 120]                       # frequencies of constant rfi
min_amp = 1.                                # min amplitude
max_amp = 5.                                # max amplitude
rfi_width = 8                               # no of channels affected by rfi