#verify the tradable stock
#load the stockpool before use this function
#!/usr/bin/env python
# encoding: utf-8
#cross section of expected stock return strategy

#make sure alter the base_info dataframe first
#  base_info = tushare.get_stock_basics()
# add tradable column for base_info dataframe
#  base_info[u'tradable] == 0
#  for i in base_info.index :
    #  if i not in stockpool[stockpool.index == stockpool.index[-1]].code:
        #  base_info.loc[i,u'tradeble'] = 0
    #  else:
        #  base_info.loc[i,u'tradeble'] = 1
import pandas as pd
import tushare
import easyquotation as eq
import sys
sys.path.append('/data/pyquant/')
from base_info import base_info as bi
import stockpool
from tradable import *

def cser():
    base_info, data = tradable()
    base_info = base_info[base_info.pb > 0]
    base_info[u'factor'] = base_info.totals * base_info.pb * base_info.pb * base_info.price
    return base_info.sort([u'factor'])[:10]

def jiyougu():
    base_info, data = tradable()
    base_info = base_info[base_info.pb > 0]
    base_info = base_info[base_info.pe > 0]
    base_info[u'factor'] = base_info.totals * base_info.pb * base_info.pe
    return base_info.sort([u'factor'])[:10]

def lajigu():
    base_info, data = tradable()
    base_info = base_info[base_info.pb > 0]
    base_info = base_info[base_info.pe <= 0]
    base_info[u'factor'] = base_info.totals * base_info.pb
    return base_info.sort([u'factor'])[:10]

def paomo(base_info):
    base_info = base_info[base_info.pb > 0]
    base_info = base_info[base_info.pe > 0]
    base_info[u'factor'] = base_info.pb * base_info.pe
    return base_info.sort([u'factor']).tail(10)

def zhenfu():
    file_name1 = '/home/way/signal/zhenfu'
    with open(file_name1) as f:
        eryue = str(f.readlines()[0])
    s = stockpool.Stockpool()
    mondata = s.load(table=eryue, day=120)
    base_info = bi()

    trade_days = pd.DataFrame(mondata.groupby(u'code').size(), columns=['trade_days'])
    base_info[u'trade_days'] = trade_days.trade_days
    base_info = base_info[base_info.pb > 0]
#    base_info = base_info[base_info.trade_days > 20]
    base_info[u'high'] = mondata.groupby(u'code').high.max()
    base_info[u'low'] = mondata.groupby(u'code').low.min()
    base_info[u'cha'] = base_info.high - base_info.low
    base_info = base_info[base_info.cha > 0]
#    base_info = base_info[base_info.timeToMarket < 20151111]
    base_info['zhenfu'] = base_info.cha / base_info.low
    base_info[u'factor'] = base_info.markter_value * base_info.pb / base_info.zhenfu
    return base_info.sort([u'factor'])[:5]

def prezhenfu(base_info, mondata):

    trade_days = pd.DataFrame(mondata.groupby(u'code').size(), columns=['trade_days'])
    base_info[u'trade_days'] = trade_days.trade_days
    base_info = base_info[base_info.pb > 0]
#    base_info = base_info[base_info.trade_days > 10]
    base_info[u'high'] = mondata.groupby(u'code').high.max()
    base_info[u'low'] = mondata.groupby(u'code').low.min()
    base_info[u'cha'] = base_info.high - base_info.low
    base_info = base_info[base_info.cha > 0]
    base_info[u'factor'] = base_info.totals * base_info.pb * base_info.price * base_info.change * base_info.low / base_info.cha
    return base_info.sort([u'factor'])[:5]

def xiaoshizhi():
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
    base_info = base_info[base_info.market > 0]
    base_info = base_info[base_info.name.str.contains('ST')*1 == 0]
    base_info = base_info[base_info.name.str.contains('退市')*1 == 0]
    base_info = base_info.sort_values(by=['market'])
    stock = base_info[base_info.market <= 1000000]
    return stock
