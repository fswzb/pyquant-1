#!/usr/bin/env python
# encoding: utf-8

#verify the tradable stock
#load the yesterdayline before use this function
import tushare

def tradable(yesterdayline):

    base_info = tushare.get_stock_basics()
    yesterdayline['limit'] = yesterdayline.high - yesterdayline.low
    yesterdayline = yesterdayline[yesterdayline.limit != 0]
    base_info[u'price'] = 0
    base_info.price = yesterdayline.close
    base_info = base_info.dropna()
    
# add tradable column for base_info dataframe
#    base_info[u'tradable'] = 0
#    base_info[u'price'] = 0
#    for i in yesterdayline.index :
#        base_info.loc[i,u'tradable'] = 1
#        base_info.loc[i, u'price'] = yesterdayline.loc[i, u'close']
            
    return base_info


