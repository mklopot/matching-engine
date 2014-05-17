#!/usr/bin/python

import cmd
import shlex

class market_shell(cmd.Cmd):
    user = None

    def do_user(self,args):
        tokens = shlex.split(args)
        if len(tokens) == 0:
            if not self.user:
                print "Currently not logged in"
            else:
                print "Currently logged in as {}".format(self.user)
            
        elif len(tokens) == 2:
            user = tokens[0]
            password = tokens[1]
            userlist = filter(lambda u: u.id == user,users)
            if userlist: 
                userobject = userlist.pop()
                if userobject.password == password:
                    self.user = user 
                    print "Successfully logged in as {}".format(self.user)
                else:
                    print "Failed to log in as {}".format(user)
            else:
                print "Failed to log in as {}".format(user)
        else:
            self.help_user()

    def help_user(self,**args):
        print "Usage: user <username> <password>"
        print "Log in with a username and password"
        print
        print "Usage: user"
        print "Display current user ID"

    def auth(self):
        if not self.user:
            print "You must be logged in to use this function"
            return False
        else:
            return True

    def do_buy(self,args):
        if self.auth():    
            args = shlex.split(args)
            num_args = len(args)
            if num_args == 1:
                try:
                    args[0] = float(args[0])
                except ValueError:
                    self.help_buy()
                    return
                print "Placing a market BUY order for {0[0]} unit(s)".format(args)
            elif num_args == 3 and args[1] in ["@", "limit"]:
                try:
                    args[0] = float(args[0])
                    args[2] = float(args[2])
                except ValueError:
                    self.help_buy()
                    return
                print "Placing a limit BUY order for {0[0]} unit(s) at {0[2]} or better".format(args)
            else:
                self.help_buy()

    def help_buy(self,**args):
        print "Usage: buy <units>"
        print "Place a BUY market order"
        print 
        print "Usage: buy <units> limit <limit price>"
        print "Place a BUY limit order"

    def do_sell(self,args):
        if self.auth():
            args = shlex.split(args)
            num_args = len(args)
            if num_args == 1:
                try:
                    args[0] = float(args[0])
                except ValueError:
                    self.help_sell()
                    return
                print "Placing a market SELL order for {0[0]} unit(s)".format(args)
            elif num_args == 3 and args[1] in ["@", "limit"]:
                try:
                    args[0] = float(args[0])
                    args[2] = float(args[2])
                except ValueError:
                    self.help_sell()
                    return
                print "Placing a limit SELL order for {0[0]} unit(s) at {0[2]} or better".format(args)
            else:
                self.help_sell()

    def help_sell(self,**args):
        print "Usage: sell <units>"
        print "Place a SELL market order"
        print 
        print "Usage: sell <units> limit <limit price>"
        print "Place a SELL limit order"

 
    def do_exit(self,args):
        print "\n"
        return -1

    def help_exit(self,**args):
        print "Usage: exit"
        print "Terminates the current session"
        print

    do_EOF = do_exit
    help_EOF = help_exit

    def preloop(self):
        self.do_help("")




if __name__ == "__main__":
    global users
    class User(object):
        id = None
        password = None

    mike=User()
    mike.id = "Mike"
    mike.password="password"
    users = [mike]

    cli = market_shell()
    cli.preloop
    cli.prompt = "> "
    cli.cmdloop("Welcome to the Market! \nUse 'buy' and 'sell' commands to place orders.\n")

