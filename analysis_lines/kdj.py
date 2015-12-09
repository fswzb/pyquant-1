#!/usr/bin/env python
# encoding: utf-8
import pandas as pd
import ema

def kdj(stock):
    low_list = pd.rolling_min(stock.low, 9)
    low_list.fillna(value = pd.expanding_min(stock.low), inplace = True)
    high_list = pd.rolling_max(stock.high, 9)
    high_list.fillna(value = pd.expanding_max(stock.high), inplace = True)
    rsv = (stock.close - low_list) / (high_list - low_list) * 100
    k = pd.ewma(rsv, com =2)
    d = pd.ewma(k, com =2)
    j = 3 * k[2:] - 2 *d

    return k, d, j
