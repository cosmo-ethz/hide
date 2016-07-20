# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Nov 9, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

#TODO: deprecated, needs to be either adjusted to new seek structure or simply removed 

def apply_gain(ctx):
    """
    Logaritmizes the data, adds an fix offset and finally applies a model of a
    standing wave to the TOD :param ctx:
    """
    
    ctx.tod_vx = np.log(ctx.tod_vx) / np.log(ctx.params.log_base)
    ctx.tod_vx += ctx.params.offset_baseline
    
    sw = get_sw(ctx.frequencies, 
                     ctx.params['model_sw'],
                     ctx.params['model_fmin'], 
                     ctx.params['model_fmax'],
                     ctx.params['model_nf'], 
                     ctx.params['model_slope'])
    
    ctx.tod_vx += sw
    ctx.tod_vy = ctx.tod_vx.copy()
    
def apply_background(ctx):
    pass
    
def get_sw(frequencies, ft_model, fmin, fmax, nf, slope):
    model_freqs = np.linspace(fmin, fmax, nf)
    model_hat = np.zeros(nf, dtype = 'complex')
    n = len(ft_model)
    model_hat[1 : n + 1] = ft_model[:n]
    model_hat[-n:] = np.conjugate(ft_model[:n])[::-1]
    model = np.fft.ifft(model_hat).real
    model += slope * model_freqs
    model -= model.mean()
    return np.interp(frequencies, model_freqs, model).reshape(-1,1)