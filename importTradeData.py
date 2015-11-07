# -*- coding: utf-8 -*-
"""
Created on Wed Oct 07 09:21:05 2015

@author: Fuqian
"""

from sqlalchemy import create_engine
import tushare as ts
#import pymongo
import pandas as pd



df_base = ts.get_stock_basics()

df_report_1503 = ts.get_report_data(2015,3)

df_profit_1503 = ts.get_profit_data(2015,3)

df_growth_1503 = ts.get_growth_data(2015,3)

#detail_daily={}

engine = create_engine('mysql://root:6598518@127.0.0.1/stock?charset=utf8')


for row_index, row in df_base.iterrows():
    try:
        f = open('qfq_err', 'a')
        f_d = open('detailDay_err','a')
        
        stocknum = row_index
        timeToMarket = df_base.ix[stocknum]['timeToMarket']
        
        startTime = str(timeToMarket)
        startTime = startTime[:4] + '-' + startTime[4:6] + '-' + startTime[6:8]
        qfq_history= ts.get_h_data(stocknum, start = startTime, end = '2015-10-09', retry_count=10)

    except:
        s = stocknum +'\n'
        
        f.write(s)
        f.close()
        pass
    else:
        qfq_history.to_sql('qfq' + stocknum,engine,if_exists='append')
 
        for row_index, row in qfq_history.iterrows():
            try:
                iqurydate = str(row_index)
                iqurydate = iqurydate[:10]
                if stocknum == '000001':
                    pass
                else:
                    detail_daily_B = ''
                    detail_daily_A = ts.get_tick_data(stocknum, date = iqurydate, retry_count = 10, pause=1)
                    detail_daily_A.insert(0,'date',iqurydate)
                    if type(detail_daily_B) is type(df_base):
                        detail_daily_B = pd.concat([detail_daily_B, detail_daily_A])
                        
                    else:
                        detail_daily_B = detail_daily_A
                        
#                    detail_daily[iqurydate] = detail_daily_A.values ##use for mongo db
#                    
#              
            except:
                s = iqurydate + ' ' + stocknum + '\n'
               
                f_d.write(s)
                
                pass
            
        detail_daily_B.to_sql('detailDay' + stocknum,engine,if_exists='append')
            
    finally:
       f.close() 
       f_d.close()
       
            
            
#            else:
#                detail_daily.to_sql('detailDay' + stocknum,engine,if_exists='append')
#        qfq_history[stocknum].to_sql('qfq' + stocknum,engine,if_exists='append')