#!/usr/bin/env python
# encoding: utf-8

import numpy as np

def sma(n, array):
    weights = np.ones(n) / n
    return np.convolve(weights, array)[n-1 : -n + 1]
