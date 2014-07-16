#!/usr/bin/python

import shell
from  marketplace import Marketplace 
from model import Session

import SocketServer
import threading

dbsession = Session()
marketplace_instance = Marketplace(dbsession)

class MyTCPHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        cli = shell.marketplace_shell(None,self.rfile,self.wfile,marketplace_instance) 
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

    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = ThreadedTCPServer((HOST, PORT), MyTCPHandler)
    print "Starting server..."

    tcp_thread = threading.Thread(target=server.serve_forever)
    tcp_thread.daemon = True
    tcp_thread.start()

#    i = 0
    while True:
#        print i; i+=1
        marketplace_instance()
#        for m in marketplace_instance.markets:
#            print m
