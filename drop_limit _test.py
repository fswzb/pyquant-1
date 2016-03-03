# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 14:04:36 2016
test drop limit when the index drop more than 2 point,clear all the holding stocks

1:开仓，2，闭仓，4，持仓，8，空仓
@author: way
"""

import tushare as ts

from count_trade_windows import *

zxb_kline = ts.get_hist_data('sh')



zxb_kline['pre_close'] = zxb_kline.close.shift(-1)

zxb_kline['pre_open'] = zxb_kline.open.shift(-1)

zxb_kline['max_drop'] = (zxb_kline.low - zxb_kline.pre_close) / zxb_kline.pre_close * 100

zxb_kline['open_drop'] = (zxb_kline.open - zxb_kline.pre_close) / zxb_kline.pre_close * 100

zxb_kline['today_change'] = (zxb_kline.close - zxb_kline.open) / zxb_kline.open * 100


zxb_kline['trade_window'] = 1

zxb_kline['kaicang'] = 0

zxb_kline['bicang'] = 0

zxb_kline['zhiyou'] = 0

zxb_kline['kongcang'] = 0
 




zxb_kline = zxb_kline[::-1]


j = 8
l = -1.39
for i in zxb_kline.index:
    if j > 2 and zxb_kline.loc[i,'kaicang'] == 0 and zxb_kline.loc[i,'open_drop'] >= l:
        zxb_kline.loc[i,'kaicang'] = 1
        zxb_kline.loc[i,'p_change'] = zxb_kline.loc[i,'today_change']
        
    elif j <= 2 and zxb_kline.loc[i,'open_drop'] <= l:
        zxb_kline.loc[i,'bicang'] = 4
        zxb_kline.loc[i,'p_change'] = zxb_kline.loc[i,'open_drop']
        
    elif j <= 2 and zxb_kline.loc[i,'max_drop'] <= l:
        zxb_kline.loc[i,'bicang'] = 4
        zxb_kline.loc[i,'p_change'] = l
    elif j <= 2 and zxb_kline.loc[i,'max_drop'] > l:
        zxb_kline.loc[i,'zhiyou'] = 2
    else:
        zxb_kline.loc[i,'kongcang'] = 8
        zxb_kline.loc[i,'p_change'] = 0
        
    j = zxb_kline.loc[i,'kaicang'] + zxb_kline.loc[i,'bicang'] + zxb_kline.loc[i,'zhiyou'] + zxb_kline.loc[i,'kongcang']

zxb_kline['next_day'] = zxb_kline.p_change.shift(-1)

zxb_kline.dropna(inplace = True)

shouyi = (zxb_kline.next_day / 100 + 1).cumprod()

yuqi = shouyi.tail(1)
#计算交易成本


yuqi = yuqi * (0.997 ** (zxb_kline.kaicang.sum() + 10))

print(yuqi)