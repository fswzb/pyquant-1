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



df_base = ts.get_stock_basics()


control_num=0

engine = create_engine('mysql://root:6598518@127.0.0.1/stock?charset=utf8')

def getDayLine(from_num, to_num, endDay):

    global df_base, control_num, engine
    for row_index, row in df_base.iterrows():
        try:
            if control_num < from_num:
                pass
            elif control_num == to_num:
                break
            else:
        
                stocknum = row_index
                timeToMarket = df_base.ix[stocknum]['timeToMarket']
                
                startTime = str(timeToMarket)
                startTime = startTime[:4] + '-' + startTime[4:6] + '-' + startTime[6:8]
                qfq_history= ts.get_h_data(stocknum, start = startTime, end = endDay, retry_count=10)
                qfq_history.insert(0,'stocknum',stocknum)
                qfq_history.to_sql('qfq_day',engine,if_exists='append')
            control_num += 1
        
    
        except:
            s = stocknum +'\n'
            f = open('qfq_err', 'a')
            f.write(s)
            f.close()
            pass
    
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
