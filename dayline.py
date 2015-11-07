# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 11:39:10 2015

@author: way
"""

#download the DAY line of all stock

from sqlalchemy import create_engine
import tushare as ts
#import pymongo
import pandas as pd

import os
import os.path

import time



df_base = ts.get_stock_basics()


control_num=0

engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')

def getDayLine(from_num, to_num,startDay = 0, endDay = time.strftime('%Y-%m-%d', time.localtime())):

    global df_base, control_num, engine
    for row_index, row in df_base.iterrows():
        try:
            if control_num < from_num:
                pass
            elif control_num == to_num:
                break
            else:
        
                stocknum = row_index
                if startDay == 0: #download the day line data from the beginning
                    
                    timeToMarket = df_base.ix[stocknum]['timeToMarket']
                    
                    startDay = str(timeToMarket)
                    startDay = startDay[:4] + '-' + startDay[4:6] + '-' + startDay[6:8]
                    
                    
                qfq_history= ts.get_h_data(stocknum, start = startDay, end = endDay, retry_count=10)
                qfq_history.insert(0,'stocknum',stocknum)
                qfq_history.to_sql('qfq_day',engine,if_exists='append')
            control_num += 1
        
    
        except:
            s = stocknum +'\n'
            f = open('qfq_err' + endDay, 'a')
            f.write(s)
            f.close()
            pass
def recoveDayline(startDay, endDay):
    global df_base, control_num, engine
    if os.path.exists('qfq_err' + endDay):
        f = open('qfq_err' + endDay)
        lines = f.readlines()
        lineNos = range(len(lines))
        
        for lineNo in lineNos:
            try:
                
                line = lines[0]
                stocknum = line[:6]
                if startDay == 0:
                    timeToMarket = df_base.ix[stocknum]['timeToMarket']
                    startDay = str(timeToMarket)
                    startDay = startDay[:4] + '-' + startDay[4:6] + '-' + startDay[6:8]
                qfq_history = ts.get_h_data(stocknum, start = startDay, end = endDay, retry_count=10)
                qfq_history.insert(0,'stocknum',stocknum)
                qfq_history.to_sql('qfq_day',engine,if_exists='append')
                del lines[0] #delect the recovered data
                print(lineNo)
                
            except:
                f.close()
                f = open('qfq_err' + endDay, 'w')
                f.writelines(lines)
                f.close()
        if os.path.getsize('qfq_err' + endDay) == 0: 
            os.remove('qfq_err' + endDay)
            
            
            
if _name_ == '_main_':
    startDay = endDay = time.strftime('%Y-%m-%d', time.localtime())
    getDayLine(0, len(df_base.index), startDay, endDay)
    recoveDayline(startDay, endDay)
    
         
            
            
    

#qfq_base = ''
#
#for stocknum in qfq_history:
#    qfq_history[stocknum].insert(0,'stocknum',stocknum)
#    if type(qfq_base) is type(df_base):
#        qfq_base = pd.concat([qfq_base, qfq_history[stocknum]])
#    else:
#        qfq_base = qfq_history[stocknum]
#        
#qfq_base.to_sql('dayline',engine,if_exists='append')
#        
