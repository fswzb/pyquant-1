#!/usr/bin/env python
# encoding: utf-8

import tushare as ts
import easytrader as et
import time
user = et.use('ht')
user.prepare('ht.json')

def check_trader():
    global position
    for stock in position:
        if stock['stock_code'] == '603299' and stock['market_value'] == 0.0:
            return True
            
def get_amount():
    global position
    for stock in position:
        if stock['stock_code'] == '603299':
            return stock['current_amount']
            
def get_entrust_id():
    entrust_list = user.entrust
    for term in entrust_list:
        if term['stock_code'] == '603299':
            return term['entrust_no']
while True:
    try:
        print(1)
        jingshen = ts.get_realtime_quotes('603299')
        preprice = float(jingshen.loc[[0], 'pre_close'])
        price = float(jingshen.loc[[0], 'price'])
        open = float(jingshen.loc[[0], 'open'])
        high = float(jingshen.loc[[0], 'high'])
        if (open - preprice) / preprice * 100 < 9.93:
            position = user.position
            sellamount = get_amount()
            print(2)
            price -= 0.01
            et.sell('603299',price = price, amount = sellamount)
            if check_trader():
                break
            else:
                entrust_id = get_entrust_id()
                user.cancel_entrust(entrust_id)
                
        if price < high:
            position = user.position
            sellamount = get_amount()
            print(2)
            price -= 0.01
            et.sell('603299',price = price, amount = sellamount)
            if check_trader():
                break
            else:
                entrust_id = get_entrust_id()
                user.cancel_entrust(entrust_id)    
    except:
        pass
    
    time.sleep(1)



