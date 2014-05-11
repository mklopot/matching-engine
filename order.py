#!/usr/bin/python

import datetime

class Order(object):
    def __init__(self,user,size=1):
        self.user = user
        self.size = size
        self.created_time = datetime.datetime.now().strftime('%s%f')
        self.submitted_time = False
        self.status = "Not Submitted"
        self.filled_at = None
        self.filled_by = None

    def __str__(self):
        return "{0} submitted:{1.submitted_time} for {1.size:12.8f}  created:{1.created_time}  user:{1.user:10} status:{1.status:16}".format(type(self).__name__,self)

class LimitOrder(Order):
    def __init__(self,user,limit,size=1):
        super(LimitOrder, self).__init__(user,size)
        self.limit = limit

    def __str__(self):
        return "{0} at {1.limit:6.2f} for {1.size:12.8f}  created:{1.created_time}  submitted:{1.submitted_time}  user:{1.user:10} status:{1.status:16}".format(type(self).__name__,self)

class MarketOrder(Order):
    pass

class Orderbook(object):
    def __init__(self):
        self.orderlist = []

    def __str__(self):
        s = "{} with {} order(s):\n".format(type(self).__name__, len(self.orderlist))
        for order in self.orderlist:
            s = s + str(order) + "\n"
        return s

class BuyLimitOrderbook(Orderbook):
    def add(self,order):
        if order not in self.orderlist:
            self.orderlist.append(order)
            self.orderlist.sort(key=lambda k: k.limit)
            order.submitted_time = datetime.datetime.now().strftime('%s%f')
            order.status = "Open Submitted"

class SellLimitOrderbook(Orderbook):
    def add(self,order):
        if order not in self.orderlist:
            self.orderlist.append(order)
            self.orderlist.sort(key=lambda k: k.limit, reverse=True)
            order.submitted_time = datetime.datetime.now().strftime('%s%f')
            order.status = "Open Submitted"
    
class MarketOrderbook(Orderbook):
    """This class implements both BUY and SELL orederbooks for market orders. Market orders are ordered by time of submission"""

    def add(self,order):
        if order not in self.orderlist:
            self.orderlist.insert(0,order)
            order.submitted_time = datetime.datetime.now().strftime('%s%f')
            order.status = "Open Submitted"

class MatchingEngine(object):
    def __init__(self):
        self.sell_limitbook = SellLimitOrderbook()
        self.buy_limitbook = BuyLimitOrderbook()
        self.sell_marketbook = MarketOrderbook()
        self.buy_marketbook = MarketOrderbook()
        self.filled = []
        self.reference_price = False
 
    def match(self):
        # Market orders on the BUY side get processed first
        if self.buy_marketbook:
            # If a SELL market order exists, try match it. To determine price, a limit SELL order or a refernece price must exist.
            if self.sell_marketbook and (self.sell_limitbook or self.reference_price):
                if self.buy_marketbook[-1].size < self.sell_marketbook[-1].size:
                    buy_order = self.buy_marketbook.pop()
                    sell_order_orig = self.sell_marketbook[-1]
                    # Update user objects here (account balances, etc)
                    sell_order_filled = sell_order_orig.copy()
                    sell_order_filled.size = buy_order.size
                    sell_order_orig -= buy_order.size
                    buy_order.status = "Filled"
                    sell_order_filled.status = "Filled Partial"
                    sell_order_orig.status = "Open Partial"
                    self.filled.append(buy_order)
                    self.filled.append(sell_order_filled)
                    if self.sell_limitbook:
                        price = self.sell_limitbook[-1].limit
                        buy_order.filled_at = sell_order_filled.filled_at = price
                    else:
                        buy_order.filled_at = sell_order_filled.filled_at = self.reference_price
                    buy_order.filled_at = sell_order_filled.filled_at = datetime.datetime.now().strftime('%s%f')
                    buy_order.filled_by = sell_order_filled
                    sell_order_filled.filled_by = buy_order                    


if __name__ == "__main__":

    limit_order1 = LimitOrder(user="Abe",limit=10,size=7)
    print limit_order1
    limit_order2 = LimitOrder(user="Boaz",limit=11.2,size=20)
    limit_order3 = LimitOrder(user="Boaz",limit=9,size=20)

    limit_order4 = LimitOrder(user="Jane",limit=15,size=2)
    limit_order5 = LimitOrder(user="Kate",limit=15.2,size=2.5)
    limit_order6 = LimitOrder(user="Lisa",limit=16,size=20)

    market_order1 = MarketOrder(user="Abe",size=.3)
    print market_order1
    market_order2 = MarketOrder(user="Boaz",size=5)
    market_order3 = MarketOrder(user="Daisy",size=4)
    market_order4 = MarketOrder(user="Carol",size=1)

    limit_orderbook1 = BuyLimitOrderbook()
    limit_orderbook1.add(limit_order1)
    limit_orderbook1.add(limit_order2)
    limit_orderbook1.add(limit_order3)
    print limit_orderbook1

    limit_orderbook2 = SellLimitOrderbook()
    limit_orderbook2.add(limit_order4)
    limit_orderbook2.add(limit_order5)
    limit_orderbook2.add(limit_order6)
    print limit_orderbook2

    market_orderbook1 = MarketOrderbook()
    market_orderbook1.add(market_order1)
    market_orderbook1.add(market_order2)
    market_orderbook1.add(market_order4)
    market_orderbook1.add(market_order3)
    print market_orderbook1

    market_orderbook2 = MarketOrderbook()
    market_order5 = MarketOrder(user="Eve",size=1.6)
    market_order6 = MarketOrder(user="Farah",size=50)
    market_order7 = MarketOrder(user="George",size=4)
    market_order8 = MarketOrder(user="Helen",size=1)
    market_orderbook2.add(market_order5)
    market_orderbook2.add(market_order6)
    market_orderbook2.add(market_order7)
    market_orderbook2.add(market_order8)
    print market_orderbook2


