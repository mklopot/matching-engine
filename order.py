#!/usr/bin/python

import datetime

class Order(object):
    def __init__(self,user,size=1):
        self.user = user
        self.size = size
        self.created_at = datetime.datetime.now().strftime('%s%f')
        self.submitted_at = None

    def __str__(self):
        return "{0} submitted:{1.submitted_at} for {1.size:12.8f}  created:{1.created_at}  user:{1.user:10}".format(type(self).__name__,self)

class LimitOrder(Order):
    def __init__(self,user,limit,size=1):
        super(LimitOrder, self).__init__(user,size)
        self.limit = limit

    def __str__(self):
        return "{0} at {1.limit:6.2f} for {1.size:12.8f}  created:{1.created_at}  submitted:{1.submitted_at}  user:{1.user:10}".format(type(self).__name__,self)

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
            order.submitted_at = datetime.datetime.now().strftime('%s%f')

class SellLimitOrderbook(Orderbook):
    def add(self,order):
        if order not in self.orderlist:
            self.orderlist.append(order)
            self.orderlist.sort(key=lambda k: k.limit, reverse=True)
            order.submitted_at = datetime.datetime.now().strftime('%s%f')
    
class MarketOrderbook(Orderbook):
    def add(self,order):
        if order not in self.orderlist:
            self.orderlist.append(order)
            order.submitted_at = datetime.datetime.now().strftime('%s%f')


if __name__ == "__main__":

    limit_order1 = LimitOrder(user="Abe",limit=10,size=7)
    print limit_order1
    limit_order2 = LimitOrder(user="Boaz",limit=11.2,size=20)
    limit_order3 = LimitOrder(user="Boaz",limit=9,size=20)

    market_order1 = MarketOrder(user="Abe",size=3)
    print market_order1
    market_order2 = MarketOrder(user="Boaz",size=5)
    print market_order2

    limit_orderbook1 = BuyLimitOrderbook()
    limit_orderbook1.add(limit_order1)
    limit_orderbook1.add(limit_order2)
    limit_orderbook1.add(limit_order2)
    limit_orderbook1.add(limit_order3)
    print limit_orderbook1
    print limit_order1
