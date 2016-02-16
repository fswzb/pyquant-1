# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 12:16:19 2016
test newly issue stock profermece after fisrt drown back

@author: way
"""
import tushare as ts
import pandas as pd
import datetime

base_info = ts.get_stock_basics()
data_b = ''
#新发行的100支股票
newly_issued = base_info.sort_values([u'timeToMarket']).tail(100)

for row_index, row in newly_issued.iterrows():
    try:
        
        stocknum = row_index
        timeToMarket = newly_issued.ix[stocknum]['timeToMarket']
        
        startTime = str(timeToMarket)
        stopTime = (datetime.datetime.strptime(startTime,"%Y%m%d") - datetime.timedelta(days = 45))
        if datetime.datetime.now() > stopTime:
            stopTime = datetime.datetime.now()
        stopTime = stopTime.strftime("%Y%m%d")
        
        startTime = startTime[:4] + '-' + startTime[4:6] + '-' + startTime[6:8]
        stopTime = stopTime[:4] + '-' + stopTime[4:6] + '-' + stopTime[6:8]
        
        
        data_a = ts.get_hist_data(stocknum, start = startTime, end = stopTime, retry_count=10)
        data_a.insert(0,'code',stocknum)
        if type(data_b) is type(base_info):
            data_b = pd.concat([data_b,data_a])
            
        else:
            data_b = data_a
            
            
    except:
        pass