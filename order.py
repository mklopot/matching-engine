#!/usr/bin/python

import datetime

class Order(object):
    def __init__(self,user,buy_assetname=None,buy_amount=None,sell_assetname=None,sell_amount=None):
        self.user = user
        self.num = None    #Order number is assigned when an order is accepted by a marketplace

        self.buy_assetname = str(buy_assetname)
        self.buy_amount = buy_amount 
        self.sell_assetname = str(sell_assetname)
        self.sell_amount = sell_amount 

        if buy_amount:
            self.ordertype = "BUY"
        elif sell_amount:
            self.ordertype = "SELL"

        self.created_time = int(datetime.datetime.now().strftime('%s%f'))
        self.submitted_time = False
        self.status = "Not Submitted"
        self.filled_time = None
        self.filled_price = None
        self.filled_by = None

    def __str__(self):
        if self.ordertype == "SELL":
            return "{1.num} {0:12} {1.ordertype:4} {1.sell_amount:12.6f} {1.sell_assetname:12} for              {1.buy_assetname:12}  user:{1.user.id:10}  status:{1.status:16}  price:{1.filled_price:}".format(type(self).__name__,self)
        else:
            return "{1.num} {0:12} {1.ordertype:4} {1.buy_amount:12.6f} {1.buy_assetname:12} for              {1.sell_assetname:12}  user:{1.user.id:10}  status:{1.status:16}  price:{1.filled_price:}".format(type(self).__name__,self)

class LimitOrder(Order):
    def __init__(self,user,limit,buy_amount=None,buy_assetname=None,sell_amount=None,sell_assetname=None):
        super(LimitOrder, self).__init__(user,buy_assetname,buy_amount,sell_assetname,sell_amount)
        self.limit = limit

    def __str__(self):
        if self.ordertype == "SELL":
            return "{1.num} {0:12} {1.ordertype:4} {1.sell_amount:12.6f} {1.sell_assetname:12}  @  {1.limit:12.6f} {1.buy_assetname:12}  user:{1.user.id:10}  status:{1.status:16}  price:{1.filled_price:}".format(type(self).__name__,self)
        else: 
            return "{1.num} {0:12} {1.ordertype:4} {1.buy_amount:12.6f} {1.buy_assetname:12}  @  {1.limit:12.6f} {1.sell_assetname:12}  user:{1.user.id:10}  status:{1.status:16}  price:{1.filled_price:}".format(type(self).__name__,self)

class MarketOrder(Order):
    pass
