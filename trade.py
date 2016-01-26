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
        try:
            balance = self.user.balance
            balance_log = self.LOGPATH + 'balance.log'
            err_log = self.LOGPATH + 'err.log'
            trade_log = self.LOGPATH + 'trade.log'
            start_time = time.strftime("%Y-%m-%d %H:%M",time.localtime())
            account_amount = balance[0]['asset_balance']
            reserve_amount = balance[0]['enable_balance']
            market_value = enable_balance[0]['market_value']
            BALANCE_LOG = open(balance_log, 'a')
            ERR_LOG = open(err_log, 'a')
            TRADE_LOG = open(trade_log, 'a')

            if reserve_amount < size * 10000:
                MASSAGE = '"%s": There is no enough to start the trade\n' %(start_time)
                BALANCE_LOG.write(MASSAGE)
                BALANCE_LOG.close()

            else:
                share = reserve_amount / size
                for stock in self.feed.load():
                    quotes = ts.get_realtime_quotes(stock)
                    price = float(quotes.loc[[0], 'price']) * 100 # the price for one hand, 100 share
                    last_price = price / 100
                    quantity = int(share // price * 100)
                    user.buy(stock, price=last_price, amount=quantity)
                    MASSAGE = '%s,%s,%f,%d\n' %(start_time, stock, last_price, quantity)
                    TRADE_LOG.write(MASSAGE)
                TRADE_LOG.close()
        except KeyError:
            pass

#stop function requres completed
    def stop(self):
        try:
            err_log = self.LOGPATH + 'err.log'
            trade_log = self.LOGPATH + 'trade.log'
            stop_time = time.strftime("%Y-%m-%d %H:%M",time.localtime())
            account_amount = balance[0]['asset_balance']
            reserve_amount = balance[0]['enable_balance']
            market_value = enable_balance[0]['market_value']
            BALANCE_LOG = open(balance_log, 'a')
            ERR_LOG = open(err_log, 'a')
            TRADE_LOG = open(trade_log, 'a')

            if market_value < 100:
                MASSAGE = '"%s": stocks have been clearred\n' %(stop_time)
                BALANCE_LOG.write(MASSAGE)
                BALANCE_LOG.close()

            else:
                share = reserve_amount / size
                for stock in self.feed.load():
                    quotes = ts.get_realtime_quotes(stock)
                    price = float(quotes.loc[[0], 'price']) * 100 # the price for one hand, 100 share
                    last_price = price / 100
                    quantity = int(share // price * 100)
                    user.buy(stock, price=last_price, amount=quantity)
                    MASSAGE = '%s,%s,%f,%d\n' %(stop_time, stock, last_price, quantity)
                    TRADE_LOG.write(MASSAGE)
                TRADE_LOG.close()
        except KeyError:
            pass



