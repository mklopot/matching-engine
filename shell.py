#!/usr/bin/python

import cmd
import shlex
import readline

class marketplace_shell(cmd.Cmd):
    user = None

    def __init__(self,complete_char,stdin,stdout,marketplace):
        cmd.Cmd.__init__(self,complete_char,stdin,stdout)
        self.marketplace = marketplace

    def do_user(self,args):
        tokens = shlex.split(args)
        if len(tokens) == 0:
            if not self.user:
                print >> self.stdout,  "Currently not logged in"
            else:
                print >> self.stdout,  "Currently logged in as {}".format(self.user.id)
            
        elif len(tokens) == 2:
            user_id = tokens[0]
            password = tokens[1]
            self.user = self.marketplace.get_user_by_userid(user_id,password)  
            if self.user:  
                print >> self.stdout,  "Successfully logged in as {}".format(self.user.id)
            else:
                print >> self.stdout,  "Failed to log in as {}".format(user_id)
        else:
            self.help_user()

    def help_user(self,**args):
        print >> self.stdout,  "Usage: user <username> <password>"
        print >> self.stdout,  "Log in with a username and password"
        print >> self.stdout,  "" 
        print >> self.stdout,  "Usage: user"
        print >> self.stdout,  "Display current user ID"
        print >> self.stdout,  "" 

    def auth(self):
        if not self.user:
            print >> self.stdout,  "You must be logged in to use this function"
            return False
        else:
            return True

    def validate_assetname(self,assetname):
        if assetname in [asset.name for asset in self.marketplace.assets]:
            return True
        else:
            return False

    def do_buy(self,args):
        if self.auth():    
            args = shlex.split(args)
            num_args = len(args)
            if num_args == 2  or (num_args == 4 and args[2] == "for"):
                # Market order: "buy 30 stilton" or "buy 30 cheddar for shrubberies"
                try:
                    args[0] = float(args[0])
                except ValueError:
                    self.help_buy()
                    return
                asset1 = args[1].upper()
                if self.validate_assetname(asset1):
                    args[1] = asset1
                else:
                    print >> self.stdout, "Unknown asset type: {}".format(args[1])
                    return
                if num_args == 2:
                    asset2 = self.user.default_currency
                    print >> self.stdout,  "Placing a market BUY order for {0[0]} {0[1]} at market price for default currency ({1})".format(args,asset2)
                    return
                else:
                    asset2 = args[3].upper()
                    if self.validate_assetname(asset2):
                        args[3] = asset2
                    else: 
                        print >> self.stdout, "Unknown asset type: {}".format(args[3])
                        return
                    if asset1 == asset2:
                        print >> self.stdout, "Cannot trade {0} for {0}".format(asset1)
                        self.help_buy()
                        return
                    print >> self.stdout,  "Placing a market BUY order for {0[0]} {0[1]} at market price in {0[3]}".format(args)

            elif args[2] in ["@", "at", "limit"] and (num_args == 4 or num_args == 5):
                # Limit order: "buy 23 munster @ 24.50" or "buy 20 brie at 18.75 pounds"
                try:
                    args[0] = float(args[0])
                    args[3] = float(args[3])
                except ValueError:
                    self.help_buy()
                    return
                asset1 = args[1].upper()
                if asset1 in [asset.name for asset in self.marketplace.assets]:
                    args[1] = asset1
                else:
                    print >> self.stdout, "Unknown asset type: {}".format(args[1])
                    return
                if num_args == 4:
                    asset2 = self.user.default_currency
                else:
                    asset2 = args[4].upper()
                    if self.validate_assetname(asset2):
                        args[4] = asset2
                    else:
                        print >> self.stdout, "Unknown asset type: {}".format(args[5])
                        return
                if asset1 == asset2:
                    print >> self.stdout, "Cannot trade {0} for {0}".format(asset1)
                    self.help_buy()
                    return
                print >> self.stdout,  "Placing a limit BUY order for {0[0]} {0[1]} at {0[3]} {1} or better".format(args,asset2)
            else:
                self.help_buy()

    def help_buy(self,**args):
        print >> self.stdout,  "Usage: buy <N> <asset1> [for <asset2>]"
        print >> self.stdout,  "Place a BUY market order"
        print >> self.stdout,  ""
        print >> self.stdout,  "Usage: buy <N> <asset1> at <limit price> [asset2]"
        print >> self.stdout,  "Place a BUY limit order"
        print >> self.stdout,  "" 

    def do_sell(self,args):
        if self.auth():
            args = shlex.split(args)
            num_args = len(args)
            if num_args == 2  or (num_args == 4 and args[2] == "for"):
                # Market order: "sell 30 stilton" or "sell 30 cheddar for shrubberies"
                try:
                    args[0] = float(args[0])
                except ValueError:
                    self.help_sell()
                    return
                asset1 = args[1].upper()
                if self.validate_assetname(asset1):
                    args[1] = asset1
                else:
                    print >> self.stdout, "Unknown asset type: {}".format(args[1])
                    return
                if num_args == 2:
                    asset2 = self.user.default_currency
                    print >> self.stdout,  "Placing a market SELL order for {0[0]} {0[1]} at market price for default currency ({1})".format(args,asset2)
                    return
                else:
                    asset2 = args[3].upper()
                    if self.validate_assetname(asset2):
                        args[3] = asset2
                    else:
                        print >> self.stdout, "Unknown asset type: {}".format(args[3])
                        return
                    if asset1 == asset2:
                        print >> self.stdout, "Cannot trade {0} for {0}".format(asset1)
                        self.help_sell()
                        return
                    print >> self.stdout,  "Placing a market SELL order for {0[0]} {0[1]} at market price in {0[3]}".format(args)

            elif args[2] in ["@", "at", "limit"] and (num_args == 4 or num_args == 5):
                # Limit order: "sell 23 munster @ 24.50" or "sell 20 brie at 18.75 pounds"
                try:
                    args[0] = float(args[0])
                    args[3] = float(args[3])
                except ValueError:
                    self.help_sell()
                    return
                asset1 = args[1].upper()
                if asset1 in [asset.name for asset in self.marketplace.assets]:
                    args[1] = asset1
                else:
                    print >> self.stdout, "Unknown asset type: {}".format(args[1])
                    return
                if num_args == 4:
                    asset2 = self.user.default_currency
                else:
                    asset2 = args[4].upper()
                    if self.validate_assetname(asset2):
                        args[4] = asset2
                    else:
                        print >> self.stdout, "Unknown asset type: {}".format(args[5])
                        return
                if asset1 == asset2:
                    print >> self.stdout, "Cannot trade {0} for {0}".format(asset1)
                    self.help_sell()
                    return
                print >> self.stdout,  "Placing a limit SELL order for {0[0]} {0[1]} at {0[3]} {1} or better".format(args,asset2)
            else:
                self.help_sell()

    def help_sell(self,**args):
        print >> self.stdout,  "Usage: sell <N> <asset1> [for <asset2>]"
        print >> self.stdout,  "Place a SELL market order"
        print >> self.stdout,  ""
        print >> self.stdout,  "Usage: sell <N> <asset1> at <limit price> [asset2]"
        print >> self.stdout,  "Place a SELL limit order"
        print >> self.stdout,  ""

    def do_balance(self,args):
        if self.auth():
            for balance in self.user.balance: print >> self.stdout, "{0.asset} {0.balance}".format(balance)
 
    def help_balance(self,**args):
        print >> self.stdout,  "Usage: balance"
        print >> self.stdout,  "List balances for the current user at this marketplace"

    def do_markets(self,args):
        i = 1
        for market in self.marketplace.markets:
            print >> self.stdout, "{0}. {1.asset1.name} <=> {1.asset2.name}".format(i,market)
            i += 1

    def help_markets(self,**args):
        print >> self.stdout,  "Usage: markets"
        print >> self.stdout,  "List asset markets available at this marketplace"


    def do_exit(self,args):
        print >> self.stdout,  "Exiting...\n"
        return -1

    def help_exit(self,**args):
        print >> self.stdout,  "Usage: exit"
        print >> self.stdout,  "Terminates the current session"
        print >> self.stdout,  ""

    do_EOF = do_exit
    help_EOF = help_exit

    def preloop(self):
        self.do_help("")




if __name__ == "__main__":

    cli = market_shell()
    cli.preloop
    cli.prompt = "> "
    cli.cmdloop("Welcome to the Market! \nUse 'buy' and 'sell' commands to place orders.\n")

