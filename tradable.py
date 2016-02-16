#!/usr/bin/env python
# encoding: utf-8

#verify the tradable stock

import tushare
import pandas as pd

def tradable():

    base_info = tushare.get_stock_basics()
    trade_info = tushare.get_today_all()
#remove the duplicates stocks and reconstruct a new df with stock code as index
    trade_info = trade_info.drop_duplicates('code')
    trade_info = pd.DataFrame(trade_info.values, columns=trade_info.columns, index=trade_info.code)
    trade_info_tradeable = trade_info[trade_info.changepercent < 9.93]
   
    base_info[u'price'] = trade_info_tradeable.trade

    base_info = base_info.dropna()

            
    return base_info