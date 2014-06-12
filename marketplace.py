#!/usr/bin/python

import itertools

import model
import market

class Marketplace(object):
    def __init__(self,dbsession):
        self.dbsession = dbsession
        self.markets = []

        # Create a market for each pair of assets
        for combo in itertools.combinations(dbsession.query(model.Asset), 2):
            self.markets.append(market.Market(dbsession, combo[0], combo[1]))        

    def get_user_by_userid(self,user_id,supplied_password):
        user = self.dbsession.query(model.User).filter(model.User.id == user_id).scalar()
        if user and user.password == supplied_password:
            return user
        else:
            return False
        
