# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 10:46:31 2016
五日线穿过十日线交易回测，从13年的大盘指数收益来看并不理想，不如全盘做多。
@author: way
"""

import tushare as ts

from count_trade_windows import *

zxb_kline = ts.get_hist_data('399101',start='2015-01-05')

zxb_kline['next_day'] = zxb_kline.p_change.shift(1)

zxb_kline['trade_window'] = 1

zxb_kline.dropna(inplace = True)

zxb_kline = zxb_kline[::-1]

condition = zxb_kline.close / zxb_kline.ma5 

zxb_kline.trade_window.where(condition > 1, 0, inplace = True)

zxb_kline.next_day.where(condition > 1, 0, inplace = True)

shouyi = (zxb_kline.next_day / 100 + 1).cumprod()

yuqi = shouyi.tail(1)
#计算交易成本
jiaoyi = count_trade_windows(zxb_kline.trade_window)

yuqi = yuqi * (0.997 ** jiaoyi)

print(yuqi)


