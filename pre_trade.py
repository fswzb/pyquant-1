#!/usr/bin/env python
# encoding: utf-8

"""
Use for start the trade between 9:15 ~ 9:25, in order to avoid slipping point
"""
import time
import trade
import easyquotation as eq


class pre_trade(object):
    def __init__(self, feed, user):
        self.feed = feed
        self.user = user
        self.LOGPATH = '/home/way/logs/'
        self.eq_user = eq.use('sina')

    def price_limit(self, stock, flag):
        quotes = self.eq_user.stocks(stock)
        bid = quotes[stock]['bid1'] # the price for one hand, 100 share
        if flag == 1:
            return bid + 0.01 #buy
        else:
            return bid - 0.01 #sell

    def start(self):
        size = len(self.feed)
        balance = self.user.balance
        reserve_amount = balance[0]['enable_balance']
        share = reserve_amount / size
        try:
            position = self.user.position
            balance = self.user.balance
            err_log = self.LOGPATH + 'err.log'
            trade_log = self.LOGPATH + 'trade.log'
            start_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
            reserve_amount = balance[0]['enable_balance']
            ERR_LOG = open(err_log, 'a')
            TRADE_LOG = open(trade_log, 'a')
            enlist = self.user.entrust
            holdstock = []
            balance = self.user.balance
            reserve_amount = balance[0]['enable_balance']
            if reserve_amount < 10000:
                MASSAGE = '"%s": There is no enough money to start the trade or the trading finished\n' %(start_time)
                ERR_LOG.write(MASSAGE)
                ERR_LOG.close()
            else:
                for stock in self.feed:
                    if stock not in holdstock:
                        price = self.price_limit(stock,1) * 100   # the price for one hand, 100 share
                        last_price = price / 100
                        quantity = int(share // price * 100)
                        self.user.buy(stock, price=last_price, amount=quantity)
                        MASSAGE = '%s,%s,%f,%d,buy\n' %(start_time, stock, last_price, quantity)
                        TRADE_LOG.write(MASSAGE)
                TRADE_LOG.close()
                time.sleep(310)
                """
                make sure the trade finished
                """
                for stock in position:
                    if int(stock['current_amount']) > 0:
                        holdstock.append(stock['stock_code'])
                if not type(enlist) is dict:
                    for en in enlist:
                        if en['stock_code'] in self.feed:
                            self.user.cancel_entrust(en['entrust_no'])
                            time.sleep(2)
                new_feed = []
                for stock in self.feed:
                    if stock not in holdstock:
                        new_feed.append(stock)
                if len(new_feed) > 0:
                    new_trade = trade.trade(new_feed,self.user)
                    new_trade.start()
        except:
            pass

    def stop(self):
        try:
            position = self.user.position
            err_log = self.LOGPATH + 'err.log'
            trade_log = self.LOGPATH + 'trade.log'
            ERR_LOG = open(err_log, 'a')
            TRADE_LOG = open(trade_log, 'a')
            balance = self.user.balance
            trade_log = self.LOGPATH + 'trade.log'
            stop_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
            account_amount = balance[0]['asset_balance']
            market_value = balance[0]['market_value']
            TRADE_LOG = open(trade_log, 'a')
            enlist = self.user.entrust
            if market_value / account_amount * 100 < 3:
                MASSAGE = '"%s": stocks have been clearred\n' %(stop_time)
                ERR_LOG.write(MASSAGE)
                ERR_LOG.close()
            elif not type(enlist) is dict:
                for en in enlist:
                    if en['stock_code'] in self.feed:
                        self.user.cancel_entrust(en['entrust_no'])

            else:
                for term in position:
                    if term['stock_code'] in self.feed:
                        quotes = self.eq_user.stocks(term['stock_code'])
                        price = quotes[term['stock_code']]['bid1']
                        pre_close = quotes[term['stock_code']]['close']
                        change = (price - pre_close) / pre_close
                        if change * 100 >= 9.93:
                            pass
                        else:
                            last_price = self.price_limit(term['stock_code'],-1) * 100 /100
                            quantity = int(term['enable_amount'])
                            if quantity > 0:
                                self.user.sell(term['stock_code'], price=last_price, amount=quantity)
                                MASSAGE = '%s,%s,%f,%d,sell\n' %(stop_time, term['stock_code'], last_price, quantity)
                                TRADE_LOG.write(MASSAGE)
                TRADE_LOG.close()
                time.sleep(350)

                new_trade = trade.trade(self.feed,self.user)
                new_trade.stop()
        except:
            pass
