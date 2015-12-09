#!/usr/bin/env python
# encoding: utf-8

import numpy as np

def ema(n, array):
    weights = np.exp(np.linspace(-1., 0., n))
    weights /= weights.sum()
    return np.convolve(weights, array)[n-1 : -n+1]
