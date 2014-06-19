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
            newmarket = market.Market(dbsession, asset1, asset2)        
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

    def submit_buy_order(self,order,assetname1,assetname2):
        assetname1 = str(assetname1)
        assetname2 = str(assetname2)
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
