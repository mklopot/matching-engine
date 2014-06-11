#!/usr/bin/python

class Marketplace(list):
    def __init__(self,marketlist=None):
        super(Marketplace, self).__init__(self)
        if marketlist:
            self.extend(marketlist)

    def add_market(self,market):
        self.append(market)

    def remove_market(self,market):
        self.remove(market)
