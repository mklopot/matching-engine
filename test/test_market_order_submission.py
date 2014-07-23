from .. import market
from .. import order


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

class Asset(object):
    def __init__(self,name):
        self.name = name

latinum = Asset("LATINUM")
zorkmid = Asset("ZORKMID")

limit_order1 = order.LimitOrder(user=abe,limit=10,buy_amount=7)
limit_order2 = order.LimitOrder(user=boaz,limit=11.2,buy_amount=20)
limit_order3 = order.LimitOrder(user=boaz,limit=9,buy_amount=20)
limit_order4 = order.LimitOrder(user=jane,limit=5,sell_amount=2)
limit_order5 = order.LimitOrder(user=kate,limit=15.2,sell_amount=2.5)
limit_order6 = order.LimitOrder(user=lisa,limit=16,sell_amount=20)
market_order1 = order.MarketOrder(user=abe,buy_amount=.3)
market_order2 = order.MarketOrder(user=boaz,buy_amount=5)
market_order3 = order.MarketOrder(user=daisy,buy_amount=4)
market_order4 = order.MarketOrder(user=carol,buy_amount=1)
market_order5 = order.MarketOrder(user=eve,sell_amount=1.6)
market_order6 = order.MarketOrder(user=farah,sell_amount=50)
market_order7 = order.MarketOrder(user=george,sell_amount=4)
market_order8 = order.MarketOrder(user=helen,sell_amount=1)

def exchange_payment_dummy_function(*args):
    return

def test_market():
    """Instantiate a market object, invoke its match() method, and submit some orders"""

    m = market.Market(exchange_payment_dummy_function, latinum, zorkmid)
    m.match()
    print market

    m.submit_order(limit_order1)
    m.submit_order(limit_order2)
    m.submit_order(limit_order3)
    m.submit_order(limit_order4)
    m.submit_order(limit_order5)
    m.submit_order(limit_order6)

    m.submit_order(market_order1)
    m.submit_order(market_order2)
    m.submit_order(market_order4)
    m.submit_order(market_order3)

    m.submit_order(market_order5)
    m.submit_order(market_order6)
    m.submit_order(market_order7)
    m.submit_order(market_order8)

