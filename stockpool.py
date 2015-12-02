#!/usr/bin/env python
# encoding: utf-8
from sqlalchemy import create_engine
import tushare as ts
import pandas as pd
import time
import datetime

class Stockpool(object):
    def __init__(self, con):
        self.con = con
        self.df_base = ts.get_stock_basics()
        self.year = 1


    def load(self, year = 1,stocktype = 'ALL'):
#        for n in xrange(len(self.df_base.index)):
#            stocknum = self.df_base.index[n]
            if self.year == 1:
                startDate = (datetime.datetime.now() - datetime.timedelta(days = 365))
            else:

                startDate = (datetime.datetime.now() - datetime.timedelta(days = year * 365))
            startDate = startDate.strftime("%Y-%m-%d")
            sql = 'select distinct date,stocknum, open, close from qfq_day where date >=" %s"' %(startDate)
            stockpool = pd.read_sql_query(sql, self.con, index_col = 'date', parse_dates = {'date' : '%Y-%m-%d'})
            stocknumlist = stockpool.stocknum.drop_duplicates(take_last = True)
            stocklist = {}
            for  row in stocknumlist:
                stocklist[row] = stockpool.loc[(stockpool['stocknum'] == row), 'open':'close']
                
            stockpanel = pd.Panel(stocklist)
#            stocklist = {}
#            stocklist[stocknum] = stock
           #stock = pd.Panel({stocknum : stock})
            #if not stock.empty:
            #    yield n, stock
            #    n = n + 1
#
#            else:
#                yield n, 'not found'
#                n = n + 1
##                pass
#    def
            return stockpanel
