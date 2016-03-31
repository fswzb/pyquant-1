#!/usr/bin/env python
# encoding: utf-8
# initize the user connect through easytrader first before using this class,
import time
import tushare as ts

class trade(object):
    def __init__(self, feed, user):
        self.feed = feed
        self.user = user
        self.LOGPATH = '/home/way/logs/'
    def start(self):
        size = len(self.feed)
        while True:
            try:
                position = self.user.position
                balance = self.user.balance
                err_log = self.LOGPATH + 'err.log'
                trade_log = self.LOGPATH + 'trade.log'
                start_time = time.strftime("%Y-%m-%d %H:%M",time.localtime())
                reserve_amount = balance[0]['enable_balance']
                ERR_LOG = open(err_log, 'a')
                TRADE_LOG = open(trade_log, 'a')
                enlist = self.user.entrust
                holdstock = []
                for stock in position:
                    if int(stock['current_amount']) > 0:
                        holdstock.append(stock['stock_code'])
                if reserve_amount < size * 10000:
                    MASSAGE = '"%s": There is no enough money to start the trade or the trading finished\n' %(start_time)
                    ERR_LOG.write(MASSAGE)
                    ERR_LOG.close()
                    break
                elif not type(enlist) is dict:
                    for en in enlist:
                        self.user.cancel_entrust(en['entrust_no'])
                else:
                    share = reserve_amount / size
                    for stock in self.feed:
                        if stock not in holdstock:
                            quotes = ts.get_realtime_quotes(stock)
                            price = float(quotes.loc[[0], 'price']) * 100 # the price for one hand, 100 share
                            last_price = price / 100
                            quantity = int(share // price * 100)
                            self.user.buy(stock, price=last_price, amount=quantity)
                            MASSAGE = '%s,%s,%f,%d,buy\n' %(start_time, stock, last_price, quantity)
                            TRADE_LOG.write(MASSAGE)
                    TRADE_LOG.close()
                    time.sleep(5)
            except:
                pass

    def stop(self):
        n = 1
        while True:
            try:
                n += 1
                if n >= 15:
                    break
                position = self.user.position
                err_log = self.LOGPATH + 'err.log'
                trade_log = self.LOGPATH + 'trade.log'
                ERR_LOG = open(err_log, 'a')
                TRADE_LOG = open(trade_log, 'a')
                balance = self.user.balance
                trade_log = self.LOGPATH + 'trade.log'
                stop_time = time.strftime("%Y-%m-%d %H:%M",time.localtime())
                account_amount = balance[0]['asset_balance']
                market_value = balance[0]['market_value']
                TRADE_LOG = open(trade_log, 'a')
                enlist = self.user.entrust
                if market_value / account_amount * 100 < 3:
                    MASSAGE = '"%s": stocks have been clearred\n' %(stop_time)
                    ERR_LOG.write(MASSAGE)
                    ERR_LOG.close()
                    break
                elif not type(enlist) is dict:
                    for en in enlist:
                        self.user.cancel_entrust(en['entrust_no'])

                else:
                    for term in position:
                        if term['stock_code'] in self.feed:
                            quotes = ts.get_realtime_quotes(term['stock_code'])
                            price = float(quotes.loc[[0], 'price']) * 100 # the price for one hand, 100 share
                            pre_close = float(quotes.loc[[0], 'price']) * 100
                            change = (price - pre_close) / pre_close
                            if change * 100 >= 9.93:
                                pass
                            else:
                                last_price = price / 100
                                quantity = int(term['enable_amount'])
                                if quantity > 0:
                                    self.user.sell(term['stock_code'], price=last_price, amount=quantity)
                                    MASSAGE = '%s,%s,%f,%d,sell\n' %(stop_time, term['stock_code'], last_price, quantity)
                                    TRADE_LOG.write(MASSAGE)
                    TRADE_LOG.close()
                    time.sleep(5)
            except:
                pass
