#!/usr/bin/env python
import SocketServer
import sys
class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        #data = raw_input()
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "%s:%d wrote:" % (self.client_address[0],self.client_address[1])
        print self.data
        # just send back the same data, but upper-cased
        body = "your ip is %s:%s, your data is %s" % (self.client_address[0], self.client_address[1], self.data.upper())     
        return_data = "HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s" % (len(body), body)
        self.request.sendall(return_data)
        # udp
        #data = self.request[0].strip()
        #socket = self.request[1]
        #socket.sendto(data.upper(), self.client_address)

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 1190
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    # server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)

    print 'listen to %s:%d ' % (HOST, PORT)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()