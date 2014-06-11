#!/usr/bin/python

import cmd
import shlex

class market_shell(cmd.Cmd):
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
                print >> self.stdout,  "Currently logged in as {}".format(self.user)
            
        elif len(tokens) == 2:
            user = tokens[0]
            password = tokens[1]
            userlist = filter(lambda u: u.id == user,users)
            if userlist: 
                userobject = userlist.pop()
                if userobject.password == password:
                    self.user = user 
                    print >> self.stdout,  "Successfully logged in as {}".format(self.user)
                else:
                    print >> self.stdout,  "Failed to log in as {}".format(user)
            else:
                print >> self.stdout,  "Failed to log in as {}".format(user)
        else:
            self.help_user()

    def help_user(self,**args):
        print >> self.stdout,  "Usage: user <username> <password>"
        print >> self.stdout,  "Log in with a username and password"
        print >> self.stdout,  "" 
        print >> self.stdout,  "Usage: user"
        print >> self.stdout,  "Display current user ID"

    def auth(self):
        if not self.user:
            print >> self.stdout,  "You must be logged in to use this function"
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
                print >> self.stdout,  "Placing a market BUY order for {0[0]} unit(s)".format(args)
            elif num_args == 3 and args[1] in ["@", "limit"]:
                try:
                    args[0] = float(args[0])
                    args[2] = float(args[2])
                except ValueError:
                    self.help_buy()
                    return
                print >> self.stdout,  "Placing a limit BUY order for {0[0]} unit(s) at {0[2]} or better".format(args)
            else:
                self.help_buy()

    def help_buy(self,**args):
        print >> self.stdout,  "Usage: buy <units>"
        print >> self.stdout,  "Place a BUY market order"
        print >> self.stdout,  ""
        print >> self.stdout,  "Usage: buy <units> limit <limit price>"
        print >> self.stdout,  "Place a BUY limit order"

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
                print >> self.stdout,  "Placing a market SELL order for {0[0]} unit(s)".format(args)
            elif num_args == 3 and args[1] in ["@", "limit"]:
                try:
                    args[0] = float(args[0])
                    args[2] = float(args[2])
                except ValueError:
                    self.help_sell()
                    return
                print >> self.stdout,  "Placing a limit SELL order for {0[0]} unit(s) at {0[2]} or better".format(args)
            else:
                self.help_sell()

    def help_sell(self,**args):
        print >> self.stdout,  "Usage: sell <units>"
        print >> self.stdout,  "Place a SELL market order"
        print >> self.stdout,  "" 
        print >> self.stdout,  "Usage: sell <units> limit <limit price>"
        print >> self.stdout,  "Place a SELL limit order"

 
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

