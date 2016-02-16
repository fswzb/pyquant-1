# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 21:43:13 2016

@author: way
"""
import tushare as ts
import time

def get_today_line():
    data = ts.get_today_all()
    filename = time.strftime('%Y-%m-%d', time.localtime()) + '.csv'
    dirp = '/data/dayline/'
    data.to_csv(dirp+filename,index=False,encoding='gbk')