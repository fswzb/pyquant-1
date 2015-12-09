#!/usr/bin/env python
# encoding: utf-8

#verify the tradable stock
#load the stockpool before use this function
import tushare

def tradable(stockpool):

    base_info = tushare.get_stock_basics()
# add tradable column for base_info dataframe
    base_info[u'tradable'] = 0
    for i in stockpool[stockpool.index == stockpool.index[-1]].stocknum :
        base_info.loc[i,u'tradable'] = 1
            
    return base_info


