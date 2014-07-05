#!/usr/bin/python

import datetime
import copy

class Order(object):
    def __init__(self,user,size=1,assetname1=None,assetname2=None,ordertype=""):
        self.user = user
        self.num = None    #Order number is assigned when an order is accepted by a marketplace
        self.size = size
        self.assetname1 = str(assetname1)
        self.assetname2 = str(assetname2)
        self.ordertype = ordertype 
        self.created_time = int(datetime.datetime.now().strftime('%s%f'))
        self.submitted_time = False
        self.status = "Not Submitted"
        self.filled_time = None
        self.filled_price = None
        self.filled_by = None

    def __str__(self):
        return "{1.num} {0:12} {1.ordertype:4} {1.size:12.6f} {1.assetname1:12} for              {1.assetname2:12}  user:{1.user.id:10}  status:{1.status:16}  price:{1.filled_price:}".format(type(self).__name__,self)

class LimitOrder(Order):
    def __init__(self,user,limit,size=1,assetname1=None,assetname2=None,ordertype=""):
        super(LimitOrder, self).__init__(user,size,assetname1,assetname2,ordertype)
        self.limit = limit

    def __str__(self):
        return "{1.num} {0:12} {1.ordertype:4} {1.size:12.6f} {1.assetname1:12}  @  {1.limit:12.6f} {1.assetname2:12}  user:{1.user.id:10}  status:{1.status:16}  price:{1.filled_price:}".format(type(self).__name__,self)

class MarketOrder(Order):
    pass

class Orderbook(list):
    def __str__(self):
        s = "{} with {} order(s):\n".format(type(self).__name__, len(self))
        for order in self:
            s = s + str(order) + "\n"
        return s

class BuyLimitOrderbook(Orderbook):
    def add(self,order):
        if order not in self:
            self.append(order)
            self.sort(key=lambda k: k.limit)
            order.submitted_time = int(datetime.datetime.now().strftime('%s%f'))
            order.status = "Open Submitted"

class SellLimitOrderbook(Orderbook):
    def add(self,order):
        if order not in self:
            self.append(order)
            self.sort(key=lambda k: k.limit, reverse=True)
            order.submitted_time = int(datetime.datetime.now().strftime('%s%f'))
            order.status = "Open Submitted"
    
class MarketOrderbook(Orderbook):
    """This class implements both BUY and SELL orederbooks for market orders. Market orders are ordered by time of submission"""

    def add(self,order):
        if order not in self:
            self.insert(0,order)
            order.submitted_time = int(datetime.datetime.now().strftime('%s%f'))
            order.status = "Open Submitted"

class Market(object):
    def __init__(self,exchange_payment,asset1,asset2):
        self.asset1 = asset1
        self.asset2 = asset2
        self.exchange_payment = exchange_payment    # Function to exchange assets between users when filling orders

        self.sell_limitbook = SellLimitOrderbook()
        self.buy_limitbook = BuyLimitOrderbook()
        self.sell_marketbook = MarketOrderbook()
        self.buy_marketbook = MarketOrderbook()
        self.filled_orders = []
        self.cancelled_orders = []

        self.preset_price = None
        self.last_price = None

    def __str__(self):
        x = "Filled Orders:\n"
        for order in self.filled_orders:
            x +=  str(order) + "\n"
        x += "Cancelled Orders:\n"
        for order in self.cancelled_orders:
            x +=  str(order) + "\n"
        return str(self.buy_marketbook) + str(self.sell_marketbook) + str(self.buy_limitbook) + str(self.sell_limitbook) + x

    def get_orders_by_user(self,user):
        result = []
        for orderbook in [self.sell_limitbook, self.buy_limitbook, self.sell_marketbook, self.buy_marketbook, self.filled_orders, self.cancelled_orders]:
            result.extend([order for order in orderbook if order.user == user])
        return result

    def get_reference_price(self):
        if self.sell_limitbook:
            return self.sell_limitbook[-1].limit
        elif self.last_price:
            return self.last_price
        elif self.preset_price:
            return self.preset_price
        else:
            return None

    def submit_market_buy(self,order):
        self.buy_marketbook.add(order)

    def submit_market_sell(self,order):
        self.sell_marketbook.add(order)

    def submit_limit_buy(self,order):
        self.buy_limitbook.add(order)

    def submit_limit_sell(self,order):
        self.sell_limitbook.add(order)

    def submit_sell_order(self,order):
        if isinstance(order,LimitOrder):
            self.submit_limit_sell(order)
        elif isinstance(order,MarketOrder):
            self.submit_market_sell(order)
        else:
            raise TypeError("Unsupported Order Type: {}".format(ordertype))

    def submit_buy_order(self,order):
        if isinstance(order,LimitOrder):
            self.submit_limit_buy(order)
        elif isinstance(order,MarketOrder):
            self.submit_market_buy(order)
        else:
            raise TypeError("Unsupported Order Type: {}".format(ordertype))
 
    def cancel_order(self,order_num,user):
        for orderbook in [self.sell_limitbook, self.buy_limitbook, self.sell_marketbook, self.buy_marketbook]:
            orders_to_cancel = [order for order in orderbook if order.user == user and order.num == order_num]
            if orders_to_cancel:
                for order in orders_to_cancel:
                    orderbook.remove(order)
                    self.cancelled_orders.append(order)
                    order.status = "Cancelled by User"
                return True

    def insufficient_funds(self,buy_orderbook,sell_orderbook,insufficient_funds_list):
        buy_order = buy_orderbook[-1]
        sell_order = sell_orderbook[-1]
        if buy_order.user in insufficient_funds_list:
            buy_order.status = "Insufficient Funds"
            self.cancelled_orders.append(buy_orderbook.pop())
        elif sell_order.user in insufficient_funds_list:
            sell_order.status = "Insufficient Funds"
            self.cancelled_orders.append(sell_orderbook.pop())

    def fill(self,buy_orderbook,sell_orderbook,unitprice):
        buy_order = buy_orderbook[-1]
        sell_order = sell_orderbook[-1]
        if buy_order.size == sell_order.size:
            insufficient_funds_list = self.exchange_payment(buy_order.user,self.asset2.name,unitprice*buy_order.size,sell_order.user,self.asset1.name,buy_order.size)
            if insufficient_funds_list: self.insufficient_funds(buy_orderbook,sell_orderbook,insufficient_funds_list); return
            buy_order = self.buy_marketbook.pop()
            sell_order = self.sell_marketbook.pop()
            buy_order.status = "Filled"
            sell_order.status = "Filled"
            self.filled.append(buy_order)
            self.filled.append(sell_order)
            buy_order.filled_time = sell_order.filled_time = int(datetime.datetime.now().strftime('%s%f'))
            buy_order.filled_by = sell_order
            sell_order.filled_by = buy_order
            self.last_price = smaller_order.filled_price = bigger_order.filled_price = unitprice
        else:
            if buy_order.size < sell_order.size:
                smaller_order = buy_order
                smaller_order_orderbook = buy_orderbook
                bigger_order = sell_order
                bigger_order_orderbook = sell_orderbook
            #    insufficient_funds_list = self.exchange_payment(buy_order.user,self.asset2.name,unitprice*buy_order.size,sell_order.user,self.asset1.name,buy_order.size)
            #    if insufficient_funds_list: self.insufficient_funds(buy_orderbook,sell_orderbook,insufficient_funds_list); return 
            elif buy_order.size > sell_order.size:
                smaller_order = sell_order
                smaller_order_orderbook = sell_orderbook
                bigger_order = buy_order
                bigger_order_orderbook = buy_orderbook

            print buy_order.user
            print sell_order.user
            print self.asset2.name
            print self.asset1.name
            print smaller_order.size
            print unitprice * smaller_order.size

            insufficient_funds_list = self.exchange_payment(buy_order.user,self.asset2.name,unitprice*smaller_order.size,sell_order.user,self.asset1.name,smaller_order.size)
            if insufficient_funds_list: self.insufficient_funds(buy_orderbook,sell_orderbook,insufficient_funds_list); return
            smaller_order_orderbook.pop()
            bigger_order_filled = copy.copy(bigger_order)
            bigger_order_filled.size = smaller_order.size
            bigger_order.size -= smaller_order.size
            smaller_order.status = "Filled"
            bigger_order_filled.status = "Filled Partial"
            bigger_order.status = "Open Partial"
            self.filled_orders.append(smaller_order)
            self.filled_orders.append(bigger_order_filled)
            bigger_order_filled.filled_time = smaller_order.filled_time = int(datetime.datetime.now().strftime('%s%f'))
            smaller_order.filled_by = bigger_order_filled
            bigger_order_filled.filled_by = smaller_order
            self.last_price = smaller_order.filled_price = bigger_order_filled.filled_price = unitprice
             


    def match(self):
        ref_price = self.get_reference_price()
        if self.buy_marketbook and not ref_price:
            return
        # Market orders on the BUY side get processed first
        if self.buy_marketbook:
            if self.sell_marketbook: 
                self.fill(self.buy_marketbook,self.sell_marketbook,ref_price)
            elif self.sell_limitbook:
                self.fill(self.buy_marketbook,self.sell_limitbook,self.sell_limitbook[-1].limit)
        elif self.buy_limitbook:
            if self.sell_marketbook:
                self.fill(self.buy_limitbook,self.sell_marketbook,self.buy_limitbook[-1].limit)
            elif self.sell_limitbook and self.buy_limitbook[-1].limit >= self.sell_limitbook[-1].limit:
                if self.buy_limitbook[-1].submitted_time <= self.sell_limitbook[-1].submitted_time:
                    unitprice = self.buy_limitbook[-1].limit
                else:
                    unitprice = self.sell_limitbook[-1].limit 
                self.fill(self.buy_limitbook,self.sell_limitbook,self.buy_limitbook[-1].limit)


if __name__ == "__main__":

    class User(object):
        def __init__(self,id):
            self.id = id

    abe = User("Abe")
    boaz = User("Boaz")
    carol = User("Carol")
    daisy = User("Daisy")
    eve = User("Eve")
    farah = User("Farah")
    george = User("George")
    helen = User("Helen")
    jane = User("Jane")
    kate = User("Kate")
    lisa = User("Lisa")

    limit_order1 = LimitOrder(user=abe,limit=10,size=7)
    print limit_order1
    limit_order2 = LimitOrder(user=boaz,limit=11.2,size=20)
    limit_order3 = LimitOrder(user=boaz,limit=9,size=20)

    limit_order4 = LimitOrder(user=jane,limit=5,size=2)
    limit_order5 = LimitOrder(user=kate,limit=15.2,size=2.5)
    limit_order6 = LimitOrder(user=lisa,limit=16,size=20)

    market_order1 = MarketOrder(user=abe,size=.3)
    print market_order1
    market_order2 = MarketOrder(user=boaz,size=5)
    market_order3 = MarketOrder(user=daisy,size=4)
    market_order4 = MarketOrder(user=carol,size=1)

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
    market_order5 = MarketOrder(user=eve,size=1.6)
    market_order6 = MarketOrder(user=farah,size=50)
    market_order7 = MarketOrder(user=george,size=4)
    market_order8 = MarketOrder(user=helen,size=1)
    market_orderbook2.add(market_order5)
    market_orderbook2.add(market_order6)
    market_orderbook2.add(market_order7)
    market_orderbook2.add(market_order8)
    print market_orderbook2

    def exchange_payment_dummy_function(*args):
        return

    class Asset(object):
        def __init__(self,name):
            self.name = name

    latinum = Asset("LATINUM")
    zorkmid = Asset("ZORKMID")

    market = Market(exchange_payment_dummy_function, latinum, zorkmid)
    market.match()
    print market

    market.submit_limit_buy(limit_order1)
    market.submit_limit_buy(limit_order2)
    market.submit_limit_buy(limit_order3)
    market.submit_limit_sell(limit_order4)
    market.submit_limit_sell(limit_order5)
    market.submit_limit_sell(limit_order6)

    market.submit_market_buy(market_order1)
    market.submit_market_buy(market_order2)
    market.submit_market_buy(market_order4)
    market.submit_market_buy(market_order3)

    market.submit_market_sell(market_order5)
    market.submit_market_sell(market_order6)
    market.submit_market_sell(market_order7)
    market.submit_market_sell(market_order8)
    
    print market
    
    while True:
        raw_input("press Enter to step...\n")
        market.match()
        print market

