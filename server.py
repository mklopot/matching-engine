#!/usr/bin/python

import shell
import marketplace as mp

import SocketServer
import threading
from sqlalchemy.orm import sessionmaker

marketplace = mp.Marketplace()

class MyTCPHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        cli = shell.market_shell(None,self.rfile,self.wfile,marketplace) 
        cli.use_rawinput = False
        cli.prompt = "> "
        cli.intro = "Welcome to the Market!\n Use 'buy' and 'sell' commands to place orders."
        cli.cmdloop()

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True


if __name__ == "__main__":

    global users
    class User(object):
        id = None
        password = None

    mike=User()
    mike.id = "Mike"
    mike.password="password"
    users = [mike]


    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = ThreadedTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()

