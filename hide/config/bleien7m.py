# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Nov 9, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals


from hide.config import bleien
from ivy.plugin.parallel_plugin_collection import ParallelPluginCollection

for name in [name for name in dir(bleien) if not name.startswith("__")]:
    globals()[name] = getattr(bleien, name)

plugins = ["hide.plugins.initialize",
           "hide.plugins.load_beam_profile",
           "hide.plugins.scanning_strategy",
           "hide.plugins.write_coords",
           "hide.plugins.write_calibration",
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
                                    "hide.plugins.add_background",
                                    "hide.plugins.background_noise",
                                    "hide.plugins.add_rfi_phaseswitch",
                                    "hide.plugins.write_tod_phaseswitch",
                                    "hide.plugins.write_rfi",
                                    "hide.plugins.clean_up",
                                     ],
                                    "hide.plugins.map_strategy_plugin",
                                    ),
           
            "ivy.plugin.show_summary_stats"
          ]

# ==================================================================
# O U T P U T
# ==================================================================
file_fmt = "TEST_{mode}_{polarization}_{date}.h5"
coordinate_file_fmt = "coord7m%s.txt"       # coordinate file name format
calibration_file_fmt = 'CALIBRATION_RSG_7m_{date}.txt' # calibration file name format
mode = 'MP'
polarizations = ['PXX']
overwrite = True

# ==================================================================
# B E A M
# ==================================================================
beam_frequency_min = 990.495025331 # 980                    # minimum frequency: [MHz]
beam_frequency_max = 1259.06610511 # 1280                   # maximum frequency: [MHz]
beam_frequency_pixscale = 0.976622108283              # pixel scale (frequency/pixel)
dish_diameter = 5.0                         # effective diameter of the dish [m]

# ==================================================================
# S C A N N I N G  S T R A T E G Y
# ==================================================================
scanning_strategy_provider = "hide.strategy.scheduler_virtual"
scheduler_file = "default"
strategy_start = "2015-12-14-00:00:00"      # survey start time. Format YYYY-mm-dd-HH:MM:SS
# strategy_end   = "2015-12-15-00:00:00"      # survey start time. Format YYYY-mm-dd-HH:MM:SS
strategy_end   = "2016-05-26-23:59:00"      # survey end time. Format YYYY-mm-dd-HH:MM:SS
strategy_step_size = 6                      # size of step in [sec]
time_range = 15*60                            # time range per file [sec]

# ==================================================================
# A S T R O
# ==================================================================
astro_signal_provider = "hide.astro.gsm_point_src"
# astro_signal_provider = "hide.astro.static_gsm"
# astro_point_srcs = ["CasA", "CygA", "SagA", "TauA", "VirA"]
astro_point_srcs = ["Virtual_CasA"]

# ==================================================================
# E A R T H
# ==================================================================
earth_signal_provider = "hide.earth.constant"
# -------------------
# c o n s t a n t 
# -------------------
earth_signal_flux = 0                       # flux of constant earth signal


# ==================================================================
# B A C K G R O U N D
# ==================================================================
elevation_model = [ 1.26321397e+10,
                   -1.71282810e+10,
                    2.79280833e+10]

# ==================================================================
# N O I S E
# ==================================================================
load_noise_template = True

# ==================================================================
# P O S T P R O C E S S I N G
# ==================================================================
instrument = "hide.spectrometer.M9703A"    # spectrometer specific gain implementation

# ==================================================================
# R F I
# ==================================================================
load_rfi_template = True
rfideltat = 5                           # Width in time for RFI [units of pixels]
rfideltaf = .5                          # Width in frequency for RFI [units of pixels]
rfiexponent = 2                         # Exponential model (1) or Gaussian model (2) for RFI
rfienhance = 1.7                        # Enhance fraction covered by RFI
rfiday = (6.0, 22.0)                    # Beginning and end of RFI day
rfidamping = 0.1                        # Damping factor of RFI during the RFI night 

