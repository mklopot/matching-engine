#!/usr/bin/python

import cmd
import shlex

class market_shell(cmd.Cmd):
    user = None

    def do_user(self,args):
        tokens = shlex.split(args)
        print tokens
#        args = args.split(" ")
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
 
    def do_exit(self,args):
        print "\n"
        return -1

    def help_exit(self,**args):
        print "Usage: exit"
        print "Terminates the current session"
        print

    do_EOF = do_exit
    help_EOF = help_exit



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
    cli.prompt = "> "
    cli.cmdloop()

