#!/usr/bin/python

import time

class Order(object):
    def __init__(self,user,size=1):
        self.user = user
        self.size = size
        self.created_at = time.time()
        self.submitted_at = None

class LimitOrder(Order):
    def __init__(self,user,limit,size=1):
        super(LimitOrder, self).__init__(user,size)
        self.limit = limit

class Orderbook(object):
    def __init__(self):
        self.orderlist = []

class LimitOrderbook(Orderbook):
    def add(self,order):
        self.orderlist.append(order)
        self.orderlist.sort(key=lambda k: k.limit)
        order.submitted_at = time.time()
    
class MarketOrderbook(Orderbook):
    def add(self,order):
        self.orderlist.append(order)
        order.submitted_at = time.time()

if __name__ == "__main__":
    limit_order1 = LimitOrder(user="Abe",limit=10,size=7)
    print str(limit_order1)
