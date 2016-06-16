#!/usr/bin/env python
# encoding: utf-8

#verify the tradable stock

import tushare
import pandas as pd
import easyquotation as eq

def tradable():
    base_info = tushare.get_stock_basics()
    user = eq.use('sina')
    data = user.all
    data = pd.DataFrame(data).T
    data = data[data.sell > 0]
    data['change'] = (data.sell - data.close) / data.close * 100
    data = data[data.change < 9.93]
    base_info[u'price'] = data.sell
    base_info = base_info.dropna()
    base_info['market'] = base_info.totals * base_info.bvps * base_info.pb
    return base_info, data
