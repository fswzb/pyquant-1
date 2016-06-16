# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 16:45:32 2016

@author: way
"""

import pandas as pd
import os
import os.path
import multiprocessing

def covert_cvs(stock_data):

    period_type = 'M'
    stock_data.index = stock_data.index.to_datetime()
    period_stock_data = stock_data.resample(period_type, how='last')
#    period_stock_data['change'] = stock_data['change'].resample(period_type, how=lambda x: (x+1.0).prod() - 1.0)
    period_stock_data['open'] = stock_data['open'].resample(period_type, how='first')
    


    period_stock_data['high'] = stock_data['high'].resample(period_type, how='max')
    period_stock_data['low'] = stock_data['low'].resample(period_type, how='min')
    period_stock_data['volume'] = stock_data['volume'].resample(period_type, how='sum')
    period_stock_data['amount'] = stock_data['amount'].resample(period_type, how='sum')
    period_stock_data = period_stock_data[period_stock_data['code'].notnull()]

    return period_stock_data
    
def covert_cvs_batch(stock_csv_list):
    inputdir = '/data/pyquant/history/day/data/'
    outputdir = '/data/pyquant/history/mon/data/'
    for stock_csv in stock_csv_list:
        csv_ext_index_start = -4
        stock_code = stock_csv[:csv_ext_index_start]
        input_csv_path = os.path.join(inputdir, stock_csv)
        df_A = pd.read_csv(input_csv_path)
#        df_A['re_date'] =df_A.date 保留最后一个交易日
        df_A.set_index(['date'],inplace=True)
        if int(stock_code) > 400000:
            stock_code = 'sh' + stock_code
        else:
            stock_code = 'sz' +stock_code
        df_A.insert(0,'code',stock_code)
        df_B = covert_cvs(df_A)
        output_csv_path = os.path.join(outputdir, stock_csv)
        df_B.to_csv(output_csv_path,index=True,encoding='gbk')
        
path = '/data/pyquant/history/day/data/'
        
stock_csv_list = [f for f in os.listdir(path) if f.endswith('.csv')]
#covert_cvs_batch(stock_csv_list)
p = multiprocessing.Process(target=covert_cvs_batch,args=(stock_csv_list[:1000],))
p.start()

m = multiprocessing.Process(target=covert_cvs_batch,args=(stock_csv_list[1000:2000],))
m.start()

n = multiprocessing.Process(target=covert_cvs_batch,args=(stock_csv_list[2000:],))
n.start()
