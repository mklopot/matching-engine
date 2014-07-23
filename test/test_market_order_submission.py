from .. import market
from .. import order

class User(object):
    def __init__(self,id):
        self.id = id

abe = User("Abe")

class Asset(object):
    def __init__(self,name):
        self.name = name

latinum = Asset("LATINUM")
zorkmid = Asset("ZORKMID")

def exchange_payment_dummy_function(*args):
    return


class Test_Market_Submit():
    def setup(self):
        self.m = market.Market(exchange_payment_dummy_function, latinum, zorkmid)

    def test_submit_market_buy(self):
        """Submit a market BUY order"""

        order1 = order.MarketOrder(user=abe,buy_assetname="LATINUM",buy_amount=7,sell_assetname="ZORKMID")
        order1.num = 1

        self.m.submit_order(order1)
        assert order1 in self.m.left_marketbook
        assert self.m.left_marketbook.count(order1) == 1
        assert order1 not in self.m.right_marketbook
        assert order1 not in self.m.left_limitbook
        assert order1 not in self.m.right_limitbook
        assert order1 not in self.m.filled_orders
        assert order1 not in self.m.cancelled_orders
        assert self.m.get_orders_by_user(abe) == [order1]

        self.m.submit_order(order1)    # The duplicate submission should get thrown away
        assert order1 in self.m.left_marketbook
        assert self.m.left_marketbook.count(order1) == 1
        assert order1 not in self.m.right_marketbook
        assert order1 not in self.m.left_limitbook
        assert order1 not in self.m.right_limitbook
        assert order1 not in self.m.filled_orders
        assert order1 not in self.m.cancelled_orders

        self.m.cancel_order(1,abe)
        assert order1 not in self.m.left_marketbook
        assert order1 not in self.m.right_marketbook
        assert order1 not in self.m.left_limitbook
        assert order1 not in self.m.right_limitbook
        assert order1 not in self.m.filled_orders
        assert order1 in self.m.cancelled_orders
        assert self.m.cancelled_orders.count(order1) == 1
        assert self.m.get_orders_by_user(abe) == [order1]


    def test_submit_market_reverse_buy(self):
        """Submit a market BUY order with assets reversed"""

        order1 = order.MarketOrder(user=abe,buy_assetname="ZORKMID",buy_amount=7,sell_assetname="LATINUM")
        order1.num = 1

        self.m.submit_order(order1)
        assert order1 in self.m.right_marketbook
        assert self.m.right_marketbook.count(order1) == 1
        assert order1 not in self.m.left_marketbook
        assert order1 not in self.m.left_limitbook
        assert order1 not in self.m.right_limitbook
        assert order1 not in self.m.filled_orders
        assert order1 not in self.m.cancelled_orders
        assert self.m.get_orders_by_user(abe) == [order1]

        self.m.submit_order(order1)    # The duplicate submission should get thrown away
        assert order1 in self.m.right_marketbook
        assert self.m.right_marketbook.count(order1) == 1
        assert order1 not in self.m.left_marketbook
        assert order1 not in self.m.left_limitbook
        assert order1 not in self.m.right_limitbook
        assert order1 not in self.m.filled_orders
        assert order1 not in self.m.cancelled_orders

        self.m.cancel_order(1,abe)
        assert order1 not in self.m.left_marketbook
        assert order1 not in self.m.right_marketbook
        assert order1 not in self.m.left_limitbook
        assert order1 not in self.m.right_limitbook
        assert order1 not in self.m.filled_orders
        assert order1 in self.m.cancelled_orders
        assert self.m.cancelled_orders.count(order1) == 1
        assert self.m.get_orders_by_user(abe) == [order1]

    def test_submit_market_sell(self):
        """Submit a market SELL order"""

        order1 = order.MarketOrder(user=abe,buy_assetname="LATINUM",sell_amount=7,sell_assetname="ZORKMID")
        order1.num = 1

        self.m.submit_order(order1)
        assert order1 in self.m.left_marketbook
        assert self.m.left_marketbook.count(order1) == 1
        assert order1 not in self.m.right_marketbook
        assert order1 not in self.m.left_limitbook
        assert order1 not in self.m.right_limitbook
        assert order1 not in self.m.filled_orders
        assert order1 not in self.m.cancelled_orders
        assert self.m.get_orders_by_user(abe) == [order1]

        self.m.submit_order(order1)    # The duplicate submission should get thrown away
        assert order1 in self.m.left_marketbook
        assert self.m.left_marketbook.count(order1) == 1
        assert order1 not in self.m.right_marketbook
        assert order1 not in self.m.left_limitbook
        assert order1 not in self.m.right_limitbook
        assert order1 not in self.m.filled_orders
        assert order1 not in self.m.cancelled_orders

        self.m.cancel_order(1,abe)
        assert order1 not in self.m.left_marketbook
        assert order1 not in self.m.right_marketbook
        assert order1 not in self.m.left_limitbook
        assert order1 not in self.m.right_limitbook
        assert order1 not in self.m.filled_orders
        assert order1 in self.m.cancelled_orders
        assert self.m.cancelled_orders.count(order1) == 1
        assert self.m.get_orders_by_user(abe) == [order1]


    def test_submit_market_reverse_sell(self):
        """Submit a market SELL order with assets reversed"""

        order1 = order.MarketOrder(user=abe,buy_assetname="ZORKMID",sell_amount=7,sell_assetname="LATINUM")
        order1.num = 1

        self.m.submit_order(order1)
        assert order1 in self.m.right_marketbook
        assert self.m.right_marketbook.count(order1) == 1
        assert order1 not in self.m.left_marketbook
        assert order1 not in self.m.left_limitbook
        assert order1 not in self.m.right_limitbook
        assert order1 not in self.m.filled_orders
        assert order1 not in self.m.cancelled_orders
        assert self.m.get_orders_by_user(abe) == [order1]

        self.m.submit_order(order1)    # The duplicate submission should get thrown away
        assert order1 in self.m.right_marketbook
        assert self.m.right_marketbook.count(order1) == 1
        assert order1 not in self.m.left_marketbook
        assert order1 not in self.m.left_limitbook
        assert order1 not in self.m.right_limitbook
        assert order1 not in self.m.filled_orders
        assert order1 not in self.m.cancelled_orders

        self.m.cancel_order(1,abe)
        assert order1 not in self.m.left_marketbook
        assert order1 not in self.m.right_marketbook
        assert order1 not in self.m.left_limitbook
        assert order1 not in self.m.right_limitbook
        assert order1 not in self.m.filled_orders
        assert order1 in self.m.cancelled_orders
        assert self.m.cancelled_orders.count(order1) == 1
        assert self.m.get_orders_by_user(abe) == [order1]


    def test_submit_limit_buy(self):
        """Submit a limit BUY order"""

        order1 = order.LimitOrder(user=abe,buy_assetname="LATINUM",buy_amount=7,sell_assetname="ZORKMID",limit=8)
        order1.num = 1

        self.m.submit_order(order1)
        assert order1 in self.m.left_limitbook
        assert order1.unitprice == 8
        assert self.m.left_limitbook.count(order1) == 1
        assert order1 not in self.m.right_limitbook
        assert order1 not in self.m.left_marketbook
        assert order1 not in self.m.right_marketbook
        assert order1 not in self.m.filled_orders
        assert order1 not in self.m.cancelled_orders
        assert self.m.get_orders_by_user(abe) == [order1]

        self.m.submit_order(order1)    # The duplicate submission should get thrown away
        assert order1 in self.m.left_limitbook
        assert self.m.left_limitbook.count(order1) == 1
        assert order1 not in self.m.right_limitbook
        assert order1 not in self.m.left_marketbook
        assert order1 not in self.m.right_marketbook
        assert order1 not in self.m.filled_orders
        assert order1 not in self.m.cancelled_orders

        self.m.cancel_order(1,abe)
        assert order1 not in self.m.left_marketbook
        assert order1 not in self.m.right_marketbook
        assert order1 not in self.m.left_limitbook
        assert order1 not in self.m.right_limitbook
        assert order1 not in self.m.filled_orders
        assert order1 in self.m.cancelled_orders
        assert self.m.cancelled_orders.count(order1) == 1
        assert self.m.get_orders_by_user(abe) == [order1]


    def test_submit_limit_reverse_buy(self):
        """Submit a limit BUY order with assets reversed"""

        order1 = order.LimitOrder(user=abe,buy_assetname="ZORKMID",buy_amount=7,sell_assetname="LATINUM",limit=8)
        order1.num = 1

        self.m.submit_order(order1)
        assert order1 in self.m.right_limitbook
        assert order1.unitprice == .125
        assert self.m.right_limitbook.count(order1) == 1
        assert order1 not in self.m.left_limitbook
        assert order1 not in self.m.left_marketbook
        assert order1 not in self.m.right_marketbook
        assert order1 not in self.m.filled_orders
        assert order1 not in self.m.cancelled_orders
        assert self.m.get_orders_by_user(abe) == [order1]

        self.m.submit_order(order1)    # The duplicate submission should get thrown away
        assert order1 in self.m.right_limitbook
        assert order1.unitprice == .125
        assert self.m.right_limitbook.count(order1) == 1
        assert order1 not in self.m.left_limitbook
        assert order1 not in self.m.left_marketbook
        assert order1 not in self.m.right_marketbook
        assert order1 not in self.m.filled_orders
        assert order1 not in self.m.cancelled_orders

        self.m.cancel_order(1,abe)
        assert order1 not in self.m.left_marketbook
        assert order1 not in self.m.right_marketbook
        assert order1 not in self.m.left_limitbook
        assert order1 not in self.m.right_limitbook
        assert order1 not in self.m.filled_orders
        assert order1 in self.m.cancelled_orders
        assert self.m.cancelled_orders.count(order1) == 1
        assert self.m.get_orders_by_user(abe) == [order1]


    def test_submit_limit_sell(self):
        """Submit a limit SELL order"""

        order1 = order.LimitOrder(user=abe,buy_assetname="LATINUM",sell_amount=7,sell_assetname="ZORKMID",limit=8)
        order1.num = 1

        self.m.submit_order(order1)
        assert order1 in self.m.left_limitbook
        assert order1.unitprice == .125
        assert self.m.left_limitbook.count(order1) == 1
        assert order1 not in self.m.right_limitbook
        assert order1 not in self.m.left_marketbook
        assert order1 not in self.m.right_marketbook
        assert order1 not in self.m.filled_orders
        assert order1 not in self.m.cancelled_orders
        assert self.m.get_orders_by_user(abe) == [order1]

        self.m.submit_order(order1)    # The duplicate submission should get thrown away
        assert order1 in self.m.left_limitbook
        assert self.m.left_limitbook.count(order1) == 1
        assert order1 not in self.m.right_limitbook
        assert order1 not in self.m.left_marketbook
        assert order1 not in self.m.right_marketbook
        assert order1 not in self.m.filled_orders
        assert order1 not in self.m.cancelled_orders

        self.m.cancel_order(1,abe)
        assert order1 not in self.m.left_marketbook
        assert order1 not in self.m.right_marketbook
        assert order1 not in self.m.left_limitbook
        assert order1 not in self.m.right_limitbook
        assert order1 not in self.m.filled_orders
        assert order1 in self.m.cancelled_orders
        assert self.m.cancelled_orders.count(order1) == 1
        assert self.m.get_orders_by_user(abe) == [order1]


    def test_submit_limit_reverse_sell(self):
        """Submit a limit SELL order with assets reversed"""

        order1 = order.LimitOrder(user=abe,buy_assetname="ZORKMID",sell_amount=7,sell_assetname="LATINUM",limit=8)
        order1.num = 1

        self.m.submit_order(order1)
        assert order1 in self.m.right_limitbook
        assert order1.unitprice == 8
        assert self.m.right_limitbook.count(order1) == 1
        assert order1 not in self.m.left_limitbook
        assert order1 not in self.m.left_marketbook
        assert order1 not in self.m.right_marketbook
        assert order1 not in self.m.filled_orders
        assert order1 not in self.m.cancelled_orders
        assert self.m.get_orders_by_user(abe) == [order1]

        self.m.submit_order(order1)    # The duplicate submission should get thrown away
        assert order1 in self.m.right_limitbook
        assert self.m.right_limitbook.count(order1) == 1
        assert order1 not in self.m.left_limitbook
        assert order1 not in self.m.left_marketbook
        assert order1 not in self.m.right_marketbook
        assert order1 not in self.m.filled_orders
        assert order1 not in self.m.cancelled_orders

        self.m.cancel_order(1,abe)
        assert order1 not in self.m.left_marketbook
        assert order1 not in self.m.right_marketbook
        assert order1 not in self.m.left_limitbook
        assert order1 not in self.m.right_limitbook
        assert order1 not in self.m.filled_orders
        assert order1 in self.m.cancelled_orders
        assert self.m.cancelled_orders.count(order1) == 1
        assert self.m.get_orders_by_user(abe) == [order1]

