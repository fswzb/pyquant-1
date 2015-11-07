import tushare as ts

class stock(object):
    def __init__(self, stocknum, time = now):
        self.stocknum = stocknum
        self.time = time

    def getStock(self):
        return self.stocknum

    def getPrice(self, time = now):
        if self.time is not time:
            return SQLP( self.stocknum, time )
        else: return REALTIME( self.stockum, time)

    def getTime(self, price):
        self.price = price
        return SQLT( self.price )

    def SQLP(self, stocknum, time):
        #SQL inqure stock price

    def SQLT(self, stocknum, price):
        #SQL inqure the time when stock price greater or equal the  given price

    def REALTIME(self, stocknum):
        df = ts.get_realtime_quotes('stocknum')
        return df.iat[0,3]

#    def __init__(self):
#        self.stocknum = 19999
#        self.price = 10
#    def getStocknum(self):
#        return self.stocknum
#    def getPrice(self):
#        return self.price
        

class trade(object):

    def __init__(self, stock, quantity): ##quantity >0 means buy , quantity <0 means sell
        self.quantity = quantity
        self.stocknum = stock.getStocknum()
        self.price = stock.getPrice()

    def getStocknum(self):
        return self.stocknum

    def getQuantity(self):
        return self.quantity

    def tradeAmount(self):
        return self.quantity * self.price




class inventory(object):
    def __init__(self, oinv = {0:0}, ninv = {0:0}): #T+1 newly brought stock put in new inverntory(ninv)

        self.oinv = oinv  # inital the stock inventory which can be traded today
        self.ninv = ninv  # inital the stock inventory which brought today

    def getInventory(self):
        return self.oinv, self.ninv

    def invChange(self, trade):
        stocknum = trade.getStocknum()
        if trade.getQuantity() > 0:
            if stocknum in self.ninv:
                ninv = self.ninv
                ninv[stocknum] = ninv[stocknum] + trade.getQuantity()
                self.ninv[stocknum] = ninv[stocknum]
            else: self.ninv[stocknum] = trade.getQuantity()

        elif trade.getQuantity() < 0: ##need to be improved
            if stocknum in self.oinv and self.oinv[stocknum] >= trade.getQuantity():
                oinv = self.oinv
                oinv[stocknum] = oinv[stocknum] + trade.getQuantity()
                self.oinv[stocknum] = oinv[stocknum]

            else: raise ValueErr('there are no enough stocks to sell')

  

class money(object):
    def __init__(self, amount = 0):
        self.amount = amount

    def getAmount(self):
        return self.amount

    def moneyChange(self, trade, fee):
        amount = self.amount
        amount = amount - trade.tradeAmount() - fee.getFee()
        self.amount = amount

        if self.amount <= 0:
            raise ValueErr(' there is no enough money')



class fee(object):
    def __init__(self, trade):
        self.mintradefee = 5 #mininum trade fee is 5 yuan
        self.tradefee = 0.0003 #0.00003 of the total trade amount
        self.changefee = 0.0000687 #0.0000687 of the total trade amount
        self.selltax = 0.001
        self.trade = trade

    def getMintradefee(self):
        return self.mintradefee

    def getTradefee(self):
        return self.tradefee

    def getChangefee(self):
        return self.changefee

    def getSelltax(self):
        return self.selltax

    def getFee(self):
        tradeAmount = abs( self.trade.tradeAmount() )
        tradefeeAmount = self.tradefee * tradeAmount
        if tradefeeAmount <= self.mintradefee:
            self.tradefeeAmount = self.mintradefee
        else: self.tradefeeAmount = tradefeeAmount

        if self.trade.tradeAmount() > 0:
            return self.tradefeeAmount + self.changefee * tradeAmount   ##buy fee
        else: return self.tradefeeAmount + self.changefee * tradeAmount + self.selltax * tradeAmount ## sell fee


def result(trade, inv, money):
    return inv.invChange(trade), money.moneyChange(trade, fee(trade))
    
    
    

    






#stock1999 = stock()

#print(stock1999.getStocknum())
trade1999 = trade(stock(), -1000)
inv = inventory({19999 : 1000}, )
mon = money(100000)

result(trade1999, inv, mon)
#mon.moneyChange(trade1999, fee1999)

print ('inventor', inv.getInventory(), 'money', mon.getAmount())







        
