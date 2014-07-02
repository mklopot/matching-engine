#!/usr/bin/python

import itertools

import model
import market

def ordernum_generator(offset):
    n = offset
    while True:
        n += 1
        yield n

class Marketplace(object):
    def __init__(self,dbsession):
        self.dbsession = dbsession

        self.markets = []
        self.markets_hash = {}
        self.markets_hash_reverse = {}

        # Create a market for each pair of assets
        self.assets = dbsession.query(model.Asset).order_by(model.Asset.name)
        for combo in itertools.combinations(self.assets, 2):
            asset1 = combo[0]
            asset2 = combo[1]
            newmarket = market.Market(self.exchange_payment, asset1, asset2)        
            self.markets.append(newmarket)        
            self.markets_hash[(str(asset1.name),str(asset2.name))] = newmarket
            self.markets_hash_reverse[(str(asset2.name),str(asset1.name))] = newmarket

        self.order_num = ordernum_generator(69105)


    def get_user_by_userid(self,user_id,supplied_password):
        user = self.dbsession.query(model.User).filter(model.User.id == user_id).scalar()
        if user and user.password == supplied_password:
            return user
        else:
            return False

    def submit_buy_order(self,order):
        assetname1 = order.assetname1
        assetname2 = order.assetname2
        if order.num:
            print "Attempting to submit an order that already has a number assigned. Rejecting..."
            return
        if (assetname1,assetname2) in self.markets_hash:
            targetmarket = self.markets_hash[(assetname1,assetname2)]
            targetmarket.submit_buy_order(order)
            order.num = self.order_num.next()            
        elif (assetname1,assetname2) in self.markets_hash_reverse:
        # Since assets are reversed, BUY becomes SELL
            targetmarket = self.markets_hash_reverse[(assetname1,assetname2)]
            targetmarket.submit_sell_order(order)
            order.num = self.order_num.next()            
        else:
            print "Failed to find a market that trades the same assets as the incoming order"
        if order.num:
            return order.num

    def get_orders_by_user(self,user):
        result = []
        for market_instance in self.markets:
            result.extend(market_instance.get_orders_by_user(user))
        return result

    def cancel_order(self,order_num,user):
        result = []
        for market_instance in self.markets:
            result.extend([market_instance.cancel_order(order_num,user)])
        if True in result:
            return True

    def exchange_payment(self,user1,assetname1,amount1,user2,assetname2,amount2):
        """User1 sends amount1 of asset1 to user2, user2 in return sends amount2 of asset2 to user1.
           If any of the users are lacking sufficinet funds, Return a list of the users with insufficient funds to preform the exchange."""

        insufficient_funds = []
        balance1 = self.dbsession.query(model.Balance.balance).with_for_update().filter(model.Balance.user==user1.id).filter(model.Balance.asset==assetname1).scalar()
        if balance1 < amount1:
            insufficient_funds.append(user1)
        balance2 = self.dbsession.query(model.Balance.balance).with_for_update().filter(model.Balance.user==user2.id).filter(model.Balance.asset==assetname2).scalar()
        if balance2 < amount2:
            insufficient_funds.append(user2)

        if insufficient_funds:
            self.dbsession.commit()
            return insufficient_funds
        else:
           self.dbsession.add_all([model.Transaction(user=user1.id,asset=assetname1,amount=-amount1),
                                   model.Transaction(user=user2.id,asset=assetname1,amount=amount1),
                                   model.Transaction(user=user2.id,asset=assetname2,amount=-amount2),
                                   model.Transaction(user=user1.id,asset=assetname2,amount=amount2)])
           self.dbsession.commit()
