# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 20:36:04 2016

@author: way
"""

import tushare as ts
from pyquery import PyQuery as pq
from sqlalchemy import create_engine
import pandas as pd
import time

stocklist = ts.get_stock_basics()
stocklist = list(stocklist.index)
stockdata ={}
baidu = 'http://gupiao.baidu.com/stock/'

stock_with_exchange_list = list(
        map(lambda stock_code: ('sh%s' if stock_code.startswith(('5', '6', '9')) else 'sz%s') % stock_code,
            stocklist))

for i in stock_with_exchange_list:
    try:
        p = pq(baidu + i, encoding="utf-8")
        stockdata[i[2:]] = p('dd').text()
    except:
        pass
    
def str2float(x):
    if x.endswith('万'):
        return float(x[:-1]) * 1
    elif x.endswith('万手'):
        return float(x[:-2]) * 1
    elif x.endswith('手'):
        return float(x[:-1]) / 10000
    elif x.endswith('亿'):
        return float(x[:-1]) * 10000
    elif x.endswith('亿手'):
        return float(x[:-2]) * 10000
    elif x.endswith('%'):
        return float(x[:-1]) * 0.01
    elif x.endswith('-'):
        return 0
    else:
        return float(x)
    
def format_response_data(stockdata):
    for stock in stockdata:
        try:
            stockdata[stock] = stockdata[stock].split()
            stockdata[stock] = list(map(str2float,stockdata[stock]))
            stockdata[stock] = dict(
                open = stockdata[stock][0],
                volume = stockdata[stock][1],
                markter_value=int(stockdata[stock][18]),
                pb=float(stockdata[stock][19]),
                )
        except:
            stockdata[stock] = dict(
                open = 0,
                volume = 0,
                markter_value=0,
                pb=0,
                )
            
    return stockdata    

s = format_response_data(stockdata)

s=pd.DataFrame(s).T
s.reset_index(inplace=True)
file_name = '/home/way/signal/jiben'
engine = create_engine('mysql://root:6598518@192.168.1.250/stock?charset=utf8')
table = 'jiben' + time.strftime('%Y%m%d', time.localtime())
s.to_sql(table,engine,if_exists='append')
f = open(file_name, 'w')
f.write(table)
f.close()

