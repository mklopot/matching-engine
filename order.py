#!/usr/bin/python

import datetime

class Order(object):
    def __init__(self,user,size=1):
        self.user = user
        self.size = size
        self.created_at = datetime.datetime.now().strftime('%s%f')
        self.submitted_at = None

    def __str__(self):
        return "{} for user:{}, size:{}, created at:{}, submitted at:{}".format(type(self).__name__,self.user,self.size,self.created_at,self.submitted_at)

    def __repr__(self):
        return "{} for user:{}, size:{}, created at:{}, submitted at:{}".format(type(self).__name__,self.user,self.size,self.created_at,self.submitted_at)

class LimitOrder(Order):
    def __init__(self,user,limit,size=1):
        super(LimitOrder, self).__init__(user,size)
        self.limit = limit

    def __str__(self):
        return "{} for user:{}, limit:{} size:{}, created at:{}, submitted at:{}".format(type(self).__name__,self.user,self.limit,self.size,self.created_at,self.submitted_at)

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

class LimitOrderbook(Orderbook):
    def add(self,order):
        self.orderlist.append(order)
        self.orderlist.sort(key=lambda k: k.limit)
        order.submitted_at = datetime.datetime.now().strftime('%s%f')
    
class MarketOrderbook(Orderbook):
    def add(self,order):
        self.orderlist.append(order)
        order.submitted_at = datetime.datetime.now().strftime('%s%f')


if __name__ == "__main__":

    limit_order1 = LimitOrder(user="Abe",limit=10,size=7)
    print str(limit_order1)
    limit_order2 = LimitOrder(user="Boaz",limit=11,size=20)
    limit_order3 = LimitOrder(user="Boaz",limit=9,size=20)

    market_order1 = MarketOrder(user="Abe",size=3)
    print str(market_order1)
    market_order2 = MarketOrder(user="Boaz",size=5)
    print str(market_order2)

    limit_orderbook1 = LimitOrderbook()
    limit_orderbook1.add(limit_order1)
    limit_orderbook1.add(limit_order2)
    limit_orderbook1.add(limit_order3)
    print limit_orderbook1
    print str(limit_order1)
