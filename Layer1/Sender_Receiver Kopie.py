__author__ = 'matsrichter'

import socket

# THIS IS A DUMMY OBJECT
class Sender_Receiver:

    def __init__(self):
        self.sendsocket = socket.socket()
        self.recvsocket = socket.socket()         # Create a socket object
        
        recvhost = socket.gethostname() # Get local machine name
        recvport = 32101                # Reserve a port for your service.
        
        sendhost = socket.gethostname()
        sendport = 12201
        
        self.sendsocket.connect((sendhost, sendport))
        
        self.recvsocket.bind((recvhost, recvport))        # Bind to the port
        self.recvsocket.listen(5)                 # Now wait for client connection.
        self.c, addr = self.recvsocket.accept()     # Establish connection with client.
        print 'Got connection from', addr
        
        
    def send(self, object):
        strobject = str(object)
        self.sendsocket.send(strobject)
        return

    def receive(self):
        print "receiving message"
        strobject = self.c.recv(1024)
        if strobject == "":
            print "No message received - waiting for one second"
            return strobject
        instruction_dict = eval(strobject)
        print instruction_dict
        return instruction_dict

    def sendFatalError(self):
        return